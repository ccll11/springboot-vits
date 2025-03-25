import asyncio
import base64
import io
import os
import gradio as gr
import utils
import argparse
import commons
from flask import Flask,request,jsonify
from models import SynthesizerTrn
from text import text_to_sequence
import torch
from torch import no_grad, LongTensor
import soundfile as sf
import json
import tqdm
from chatgpt import gpt_35_api
from flask_sqlalchemy import SQLAlchemy

def get_text(text, hps):
    text_norm, clean_text = text_to_sequence(text, hps.symbols, hps.data.text_cleaners)
    if hps.data.add_blank:
        text_norm = commons.intersperse(text_norm, 0)
    text_norm = LongTensor(text_norm)
    return text_norm, clean_text


def vits(text, language, speaker_id, noise_scale, noise_scale_w, length_scale, hps_ms, device, speakers, net_g_ms):
    if not len(text):
        return "输入文本不能为空！", None, None
    text = text.replace('\n', ' ').replace('\r', '').replace(" ", "")
    if len(text) > 500:
        return f"输入文字过长！{len(text)}>500", None, None
    if language == 0:
        text = f"[ZH]{text}[ZH]"
    elif language == 1:
        text = f"[JA]{text}[JA]"
    else:
        text = f"{text}"
    import time
    t1 = time.time()
    stn_tst, clean_text = get_text(text, hps_ms)
    with no_grad():
        x_tst = stn_tst.unsqueeze(0).to(device)
        x_tst_lengths = LongTensor([stn_tst.size(0)]).to(device)
        speaker_id = LongTensor([speaker_id]).to(device)
        audio = \
        net_g_ms.infer(x_tst, x_tst_lengths, sid=speaker_id, noise_scale=noise_scale, noise_scale_w=noise_scale_w,
                       length_scale=length_scale)[0][0, 0].data.cpu().float().numpy()
    print(f"cost: {time.time() - t1} s")
    return 22050, audio


def tts_model_init(model_dir="./model", device='cuda'):
    audio_postprocess_ori = gr.Audio.postprocess
    limitation = os.getenv("SYSTEM") == "spaces"  # limit text and audio length in huggingface spaces

    device = torch.device(device)

    hps_ms = utils.get_hparams_from_file(os.path.join(model_dir, r'config.json'))
    net_g_ms = SynthesizerTrn(
        len(hps_ms.symbols),
        hps_ms.data.filter_length // 2 + 1,
        hps_ms.train.segment_size // hps_ms.data.hop_length,
        n_speakers=hps_ms.data.n_speakers,
        **hps_ms.model)
    _ = net_g_ms.eval().to(device)
    speakers = hps_ms.speakers

    model, optimizer, learning_rate, epochs = utils.load_checkpoint(os.path.join(model_dir, r'G_953000.pth'), net_g_ms,
                                                                    None)

    return hps_ms, device, speakers, net_g_ms




app = Flask(__name__)

# 配置 MySQL 数据库连接信息
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost:3308/vits'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

class Message(db.Model):
    __tablename__ = 'message'
    message_id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=True)
    answer = db.Column(db.Text, nullable=True)
    audio_base64 = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))

with app.app_context():
    db.create_all()


@app.route('/train',methods=['POST'])
def main():
    try:
        hps_ms, device, speakers, net_g_ms = tts_model_init(device='cuda' if torch.cuda.is_available() else 'cpu')

        # 输入文本,接受到spingboot的文本
        data = request.get_json()
        message = data.get('text')
        user_id = data.get('id')
        # 接入chatgpt
        output = gpt_35_api([{'role': 'user', 'content': message}, ])

        sr, audio = vits(output, 0, torch.tensor([142]), 0.1, 0.668, 1.2, hps_ms, device,
                         speakers, net_g_ms)

        # 将音频数据写入内存中的字节流
        audio_bytes = io.BytesIO()
        sf.write(audio_bytes, audio, samplerate=sr, format='wav')
        audio_bytes.seek(0)  # 将指针移动到字节流的开头

        # 将字节流转换为 Base64
        audio_base64 = base64.b64encode(audio_bytes.read()).decode('utf-8')

        audio_data = Message(question=message,answer = output, audio_base64=audio_base64,user_id=user_id)

        try:
            db.session.add(audio_data)
            db.session.commit()
        except Exception as e:
            print(f"数据库操作失败: {e}")
            db.session.rollback()


        return jsonify({
            "status": "success",
            "message": message,
            "audio": audio_base64
        })

    except Exception as  e:
        return jsonify({
            "status":"error",
            "message":str(e)
        })



if __name__ == '__main__':
    app.run(debug=True)

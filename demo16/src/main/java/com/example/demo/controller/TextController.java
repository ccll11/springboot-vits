package com.example.demo.controller;

import com.example.demo.entity.User;
import com.example.demo.service.PythonServiceimpl;
import jakarta.servlet.http.HttpSession;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.*;

@Controller
@RequestMapping("api")
public class TextController {
    @Autowired
    private PythonServiceimpl pythonServiceimpl;

    @GetMapping("/chat")
    public String pythonForm(){
        return "chat";
    }

    @PostMapping("/train")
    public ResponseEntity<String> trainModel(@RequestBody String text , HttpSession session) {

        User user = (User) session.getAttribute("currentUser");
        // 找到user_id
        Integer user_id = user.getId();
        System.out.println("收到的文本:"+text);
        System.out.println("发送者:"+user_id);
        // 调用 Python 服务
        String pythonResponse = pythonServiceimpl.callpython(text,user_id);
//        System.out.println("Python 服务响应: " + pythonResponse);
        return ResponseEntity.ok(pythonResponse);
    }

}

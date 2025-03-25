package com.example.demo.service;

import com.example.demo.entity.PythonRequest;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.http.*;
import org.springframework.web.client.RestTemplate;

@Service
public class PythonServiceimpl implements PythonService {

    @Value("${Config.config_flask}")
    private String url;

    public String callpython(String text,Integer id){

        PythonRequest requestBody = new PythonRequest(text, id);

//        请求头
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);

//        创建请求实体
        HttpEntity<PythonRequest> request = new HttpEntity<>(requestBody, headers);

        // 使用 RestTemplate 发送 POST 请求
        RestTemplate restTemplate = new RestTemplate();
        ResponseEntity<String> response = restTemplate.postForEntity(url+"/train", request, String.class);

        // 返回 Python 服务的响应
        return response.getBody();


    }

}

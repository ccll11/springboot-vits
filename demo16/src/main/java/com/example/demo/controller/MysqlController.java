package com.example.demo.controller;

import com.example.demo.common.Result;
import com.example.demo.common.ResultGenerator;
import com.example.demo.dao.MessageDao;
import com.example.demo.entity.Message;
import com.example.demo.entity.User;
import jakarta.annotation.Resource;
import jakarta.servlet.http.HttpSession;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.ResponseBody;

import java.util.List;

@Controller
@RequestMapping("/api")
public class MysqlController {
    @Resource
    private MessageDao messageDao;

    @RequestMapping(value = "/mysql",method = RequestMethod.GET)
    @ResponseBody
    public Result<List<Message>> queryall(HttpSession session){

        User user = (User) session.getAttribute("currentUser");
        //    找到user_id
        Integer user_id = user.getId();
        List<Message> messages = messageDao.FindALL(user_id);
        return ResultGenerator.genSuccessResult(messages);
    }

}

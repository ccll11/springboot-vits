package com.example.demo.service;

import com.example.demo.dao.UserDao;
import com.example.demo.entity.User;
import jakarta.annotation.Resource;
import org.springframework.stereotype.Service;

@Service
public class UserServiceImpl implements Uerservice{
    @Resource
    private UserDao userDao;
    @Override
    public User loginService(String username, String password) {
        User user = userDao.findByUsernameAndPassword(username,password);
        // 重要信息置空
        if(user!=null){
            user.setPassword("");
        }
        return user;
    }

    @Override
    public User registService(User user) {
        if(userDao.findByUsername(user.getUsername())!=null){
            // 无法注册
            return null;
        }else{
            //返回创建好的用户对象(带id)
            User newUser = userDao.save(user);
            if(newUser != null){
                newUser.setPassword("");
            }
            return newUser;
        }
    }
}

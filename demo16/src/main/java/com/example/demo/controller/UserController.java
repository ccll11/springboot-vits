package com.example.demo.controller;

import com.example.demo.entity.User;
import com.example.demo.service.Uerservice;
import jakarta.servlet.http.HttpSession;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

@Controller
@RequestMapping("/user")
public class UserController {
    private final Uerservice userService;

    public UserController(Uerservice userService) {
        this.userService = userService;
    }

    @GetMapping("/login")
    public String showLoginForm() {
        return "login";
    }

    @PostMapping("/login")
    public String login(@RequestParam String username, @RequestParam String password, Model model , HttpSession session) {
        User user = userService.loginService(username, password);
        if (user != null) {
            session.setAttribute("currentUser", user);
            model.addAttribute("message", "登录成功！");
            return "chat";
        } else {
            model.addAttribute("message", "账号或密码错误！");
            return "login";
        }
    }

    @GetMapping("/register")
    public String showRegisterForm() {
        return "register";
    }

    @PostMapping("/register")
    public String register(@ModelAttribute User newUser, Model model) {
        User user = userService.registService(newUser);
        if (user != null) {
            model.addAttribute("message", "注册成功！");
            return "home";
        } else {
            model.addAttribute("message", "用户名已存在！");
            return "register";
        }
    }
    @GetMapping("/vits")
    public String showVitsForm() {
        return "vits";
    }
}
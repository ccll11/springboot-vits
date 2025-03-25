package com.example.demo.entity;

public class PythonRequest {
    private String text;
    private Integer id;

    // 构造方法
    public PythonRequest(String text, Integer id) {
        this.text = text;
        this.id = id;
    }

    // Getter 和 Setter
    public String getText() {
        return text;
    }

    public void setText(String text) {
        this.text = text;
    }

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }
}
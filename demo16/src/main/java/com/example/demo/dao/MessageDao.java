package com.example.demo.dao;

import com.example.demo.entity.Message;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;

import java.util.List;

@Mapper
public interface MessageDao {
    List<Message> FindALL(Integer user_id);
}

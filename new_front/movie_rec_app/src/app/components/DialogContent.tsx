"use client";
import Axios from 'axios';
import { Dialog } from '@/types';
import React, { FormEvent, useEffect, useRef, useState } from 'react';
import styles from './DialogContent.module.css';
import DialogItem from './DialogItem';
const DialogContent = () => {
    const [dialog, setDialog] = useState<Dialog[] | null>([]);
    const [userutt, setUserUtt] = useState<string>('');
    const endiv = useRef<HTMLDivElement>(null);
    const inputdiv = useRef<HTMLInputElement>(null);

    useEffect(() => {
      if (sessionStorage.getItem('session_id')) {
        // console.log(sessionStorage.getItem('session_id'))
        Axios.get("http://localhost:8000/movie_app_backend/", {
          params: {
            session_id: sessionStorage.getItem('session_id'),
          }
        }).then((response) => {
          setDialog(response.data['dialog']);
          sessionStorage.setItem('session_id', response.data['session_id']);
        })
      } else {
        Axios.get("http://localhost:8000/movie_app_backend/", {
        }).then((response) => {
          console.log(response.data['session_id'])
          setDialog(response.data['dialog']);
          sessionStorage.setItem('session_id', response.data['session_id']);
        })
      }
    }, [])
  
    useEffect(() => {
      endiv?.current?.scrollIntoView({ behavior: 'smooth' });
      inputdiv?.current?.focus();
    }, [dialog])
  
    const handleSubmit = (e: FormEvent) => {
      e.preventDefault()
      console.log(sessionStorage.getItem('session_id'))
      setDialog([...(dialog ?? [] ), { speeker: 'ユーザ', utt: userutt, isSystem: false, new : true }])
      setUserUtt('')
      Axios.post("http://localhost:8000/movie_app_backend/", {
        session_id: sessionStorage.getItem('session_id'),
        utt: userutt,
    }).then((response) => {
        setDialog(response.data);
    })
    }

  return (
    <div>
        <ul className={styles.list}>
          {dialog?.map((item, index) => (
            <DialogItem key={index} item={item} dialog={dialog} />
          ))}
        </ul>
        <div ref={endiv} />
        <form onSubmit={handleSubmit}>
          <div className={styles.launch}>
            <input className={styles.input} onChange={(e) => setUserUtt(e.target.value)} value={userutt} ref={inputdiv} />
            <button type='submit' className={styles.btn}>送信</button>
          </div>
        </form>
    </div>
  )
}

export default DialogContent

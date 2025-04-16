"use client";
import React from 'react';
import styles from './page.module.css';
import DialogContent from './components/DialogContent';
const Home = () => {

  return (
    <section className={styles.section1}>
      <div className={styles.container}>
        <DialogContent />
      </div>
    </section>
  )
}

export default Home

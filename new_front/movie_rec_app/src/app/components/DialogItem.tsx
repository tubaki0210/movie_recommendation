import { Dialog } from '@/types'
import React, { useEffect, useState } from 'react'
import styles from './DialogItem.module.css'

interface DialogItemProps {
    item: Dialog,
    dialog : Dialog[]
}

const DialogItem = ({ item,  dialog } : DialogItemProps) => {
    const [flag, setFlag] = useState<boolean>(item.new);
    
    const SplitLineBreaks = (utt : string) => {
        return utt.split('\n').map((line, index) => (
            <React.Fragment key={index}>
                {line}
                <br />
            </React.Fragment>
        ));
    };

    useEffect(() => {
        if (item.new) {
            setTimeout(() => {
                setFlag(false)
            }, 100);
        }
    },[dialog])

    return (
        <li className={`${styles.item} ${item.isSystem ? '' : styles.user} ${flag ? styles.change : ''}`}>
            <p className={`${styles.name} ${item.isSystem ? '' : styles.usertext} `}>{item.speeker}</p>
            <div className={`${styles.textwrap} ${item.isSystem ? '' : styles.usertextwrap}`}>
                <p className={styles.text}>{SplitLineBreaks(item.utt)}</p>
            </div>
        </li>
    )
}

export default DialogItem

import styles from './TextArea.module.css'

export default function TextArea({rows, cols, text, name, placeholder, handleOnChange, value}){
    return (
        <div className={styles.text_area}>
            <label htmlFor={name}>{text}</label>
            <textarea rows={rows} cols={cols} placeholder={placeholder} onChange={handleOnChange} maxLength='255' defaultValue={value}></textarea>
        </div>
    )
}
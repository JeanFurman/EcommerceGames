import styles from './Input.module.css'

export default function Input({type, text, name, placeholder, handleOnChange, value}){
    return (
        <div className={styles.input_form}>
            <label htmlFor={name}>{text}</label>
            <input type={type} name={name} placeholder={placeholder} id={name} value={value} onChange={handleOnChange}/>
        </div>
    )
}
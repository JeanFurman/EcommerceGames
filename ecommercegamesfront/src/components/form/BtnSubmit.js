import styles from './BtnSubmit.module.css'

export default function BtnSubmit({text}){
    return (
        <div>
            <button className={styles.btn_form}>{text}</button>
        </div>
    )
}
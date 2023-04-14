import styles from './Select.module.css'

export default function Select({text, name, options, handleOnChange, value}){
    return (
        <div className={styles.select_form}>
            <label htmlFor={name}>{text}</label>
            <select name={name} id={name} value={value || ''} onChange={handleOnChange}>
                    <option>Selecione um gênero</option>
                    {options.map((option, index) => (
                        <option value={option} key={index}>{option}</option>
                    ))}
            </select>
        </div>
    )
}
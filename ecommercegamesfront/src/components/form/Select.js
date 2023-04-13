import styles from './Select.module.css'

export default function Select({text, name, options, handleOnChange, value}){
    return (
        <div className={styles.select_form}>
            <label htmlFor={name}>{text}</label>
            <select name={name} id={name} value={value || ''} onChange={handleOnChange}>
                    {options.map((option) => (
                        <option value={option.id} key={option.id}>{option.name}</option>
                    ))}
            </select>
        </div>
    )
}
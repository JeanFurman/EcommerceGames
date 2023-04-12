import { Link } from 'react-router-dom'
import styles from './BtnLink.module.css'

export default function BtnLink({to, text}){
    return (
        <Link className={styles.btn} to={to}>
            {text}
        </Link>
    )
}
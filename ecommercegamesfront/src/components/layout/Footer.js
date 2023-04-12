import { FaLinkedin, FaGithub } from 'react-icons/fa'
import styles from './Footer.module.css'

export default function Footer(){
    return(
        <footer className={styles.footer}>
            <ul>
                <li><a href='https://github.com/JeanFurman' target='_blank'><FaGithub/></a></li>
                <li><a href='https://linkedin.com/in/jean-sousa-977115175/' target='_blank'><FaLinkedin/></a></li>
            </ul>
            <p>
                <span>Jean</span> &copy; 2023
            </p>
        </footer>
    )
}
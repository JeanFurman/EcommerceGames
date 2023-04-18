import { useState } from "react"
import styles from './ControleQuantidade.module.css'
import { AiFillPlusCircle, AiFillMinusCircle, AiFillCloseCircle } from 'react-icons/ai'

export default function ControleQuantidade({nome, soma, quantidade, valor, imagem, id, removeItem}){

    const [qnt, setQnt] = useState(1)

    const mudaQuantidade = (validator) => {
        if(validator === 'aumenta'){
            if(qnt < quantidade){
                setQnt(qnt + 1)
                soma(valor, validator)

            }
        }else{
            if(qnt > 1){
                setQnt(qnt - 1)
                soma(valor, validator)
            }   
        }
    }

    const remove = () =>{
        removeItem(id, valor)
    }


    return (
        <tr>
            <td>
                <div className={styles.product}>
                    <img src={`http://localhost:8001/games/imagens/${imagem}`} />
                    <div className={styles.info}>
                        <div className={styles.name}>{nome}</div>
                    </div>
                </div>
            </td>
            <td>{`R$ ${valor}`}</td>
            <td>
                <div className={styles.qtd}>
                    <button onClick={() => {mudaQuantidade('diminui')}}>
                        <AiFillMinusCircle/>
                    </button>
                    <span>{qnt}</span>
                    <button onClick={() => {mudaQuantidade('aumenta')}}>
                        <AiFillPlusCircle/>
                    </button>
                </div>
            </td>
            <td>{`R$ ${(valor * qnt).toFixed(2)}`}</td>
            <td>
                <button onClick={remove} className={styles.remove}>
                    <AiFillCloseCircle/>
                </button>
            </td>
        </tr>
                 
    )
}
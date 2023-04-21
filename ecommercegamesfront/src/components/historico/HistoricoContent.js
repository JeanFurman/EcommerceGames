import styles from './HistoricoContent.module.css'

export default function HistoricoContent({nome, quantidade, valor, imagem, total, data, row, len}){

    return (
        <tr>
            <td>
                {console.log(nome)}
                <div className={styles.product}>
                    <img src={`http://localhost:8001/games/imagens/${imagem}`} />
                    <div className={styles.info}>
                        <div className={styles.name}>{nome}</div>
                    </div>
                </div>
            </td>
            <td>{`R$ ${valor}`}</td>
            <td>
                <span className={styles.quantidade}>{quantidade}</span>
            </td>
            {len === 1 ? <>
            <td rowSpan={row}>
                <span>{data}</span>
            </td>
            <td rowSpan={row}>
                <span>{`R$ ${total}`}</span>
            </td>
            </>: <><td></td><td className={styles.linhaTd}></td></>}
            
        </tr>
                 
    )
}
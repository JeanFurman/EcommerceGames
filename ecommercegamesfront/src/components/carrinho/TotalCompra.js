import { useState } from 'react'
import styles from './TotalCompra.module.css'

export default function TotalCompra({total}){

    return (
        <>
            <div className={styles.box}>
                <header>Total da compra</header>
                <div>
                    <span>Total</span>
                    <span>R$ {parseFloat(total).toFixed(2)}</span>
                </div>
            </div>
            <button>Finalizar Compra</button>
        </>
    )
}
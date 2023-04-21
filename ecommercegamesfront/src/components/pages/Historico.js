import styles from './Historico.module.css'
import { useState, useEffect } from "react"
import HistoricoContent from '../historico/HistoricoContent'


export default function Carrinho(){

    const [vendas, setVendas] = useState([])
    var len = 1

    useEffect(() => {
        fetch('http://localhost:8001/vendas', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem("token")}`
            }
        })
        .then((resp) => resp.json())
        .then((data) => {
            setVendas(data)
        })
        .catch((err) => console.log(err))
    }, [])

    function addLen(){
        len += 1
    }

    function resetLen(){
        len = 1
    }

    return (
      <div className={styles.historico_div}>
        <section>
          <table>
            <thead>
              <tr className={styles.trheader}>
                <th>Game</th>
                <th>Preço</th>
                <th>Quantidade</th>
                <th>Data</th>
                <th>Total</th>
              </tr>
            </thead>
            <tbody>
              {vendas.length > 0 ?<>
                {vendas.map((venda) => (<>
                        {venda.carrinhos.map((carrinho) => (<>
                            <HistoricoContent valor={carrinho.game.valor} quantidade={carrinho.quantidade} 
                            nome={carrinho.game.nome} imagem={carrinho.game.imagem} total={venda.valor_total} data={venda.criado_em} len={len} row={venda.carrinhos.length}/>
                            {addLen()}
                            </>
                        ))}
                        {resetLen()}
                        <tr className={styles.linhaTr}></tr>
                        </>
                    ))}
              </>
                :<tr><td colSpan={'5'} className={styles.semItens}>Nenhuma compra no sistema</td></tr>
              }
            </tbody>
          </table>
        </section>
      </div>
    )
}
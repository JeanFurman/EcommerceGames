import styles from './Carrinho.module.css'
import TotalCompra from "../carrinho/TotalCompra"
import { useState, useEffect } from "react"
import ControleQuantidade from '../carrinho/ControleQuantidade'

export default function Carrinho(){

    const [games, setGames] = useState([])
    const [total, setTotal] = useState(0)
    const [compras, setCompras] = useState([])

    function finalizarCompra(){
      let json = []
      compras.map((compra) =>{
        json.push(JSON.stringify(compra))
      })
      fetch('http://localhost:8001/vendas', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem("token")}`
            },
            body: `[${json}]`
        })
        .then((resp) => resp.json())
        .then(() =>{
          window.location.href = 'http://localhost:3000/'
          localStorage.removeItem('carrinho')
        })
        .catch((err) => console.log(err))
    }

    function atualizarGames(){
      if(localStorage.hasOwnProperty('carrinho')){
        const data = JSON.parse(localStorage.getItem('carrinho'))
        setGames(data)
        let sum = 0
        let c = []
        data.map((d) => {
          sum += d['valor']
          c.push({"game_id": d['id'], "quantidade": 1})
        })
        setCompras(c)
        setTotal(sum)  
      }
    }

    useEffect(() => {
      atualizarGames()
    }, [])

    function remove(id, v){
      let gameData = JSON.parse(localStorage.getItem('carrinho'))
      gameData = gameData.filter((data) => data.id !== id)
      localStorage.setItem('carrinho', JSON.stringify(gameData))
      let sum = total
      setTotal(sum - v)
      setGames(games.filter((game) => game.id !== id))
      setCompras(compras.filter((compra) => compra.game_id !== id))
    }

    function getSum(valor, action){
      if(action === 'aumenta'){
        setTotal((total) => total + valor)
      }else{
        setTotal((total) => total - valor)
      }
    }

    return (
      <div className={styles.carrinho_div}>
        <section>
          <table>
            <thead>
              <tr className={styles.trheader}>
                <th>Game</th>
                <th>Preço</th>
                <th>Quantidade</th>
                <th>Total</th>
                <th>&nbsp;&nbsp;-</th>
              </tr>
            </thead>
            <tbody>
              {games.length > 0 ?<>
              {games.map((game, index) => (
                    <ControleQuantidade key={game.id} id={game.id} soma={getSum} valor={game.valor} 
                    quantidade={game.quantidade} nome={game.nome} imagem={game.imagem} removeItem={remove} index={index} compra={compras} setCompra={setCompras}/>
                ))}</>
                :<tr><td colSpan={'5'} className={styles.semItens}>Não há itens no carrinho</td></tr>
              }
            </tbody>
          </table>
        </section>
        <aside>
          <TotalCompra total={total} finalizarCompra={finalizarCompra}/>
          {console.log(compras)}
        </aside>
      </div>
    )
}
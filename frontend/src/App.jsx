import { useEffect, useState } from "react"
import axios from "axios"

const API = "http://10.142.231.104:5000"

export default function App() {

  const [token, setToken] = useState(
    localStorage.getItem("token") || ""
  )

  const [user, setUser] = useState(null)

  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")

  const [receiver, setReceiver] = useState("")
  const [amount, setAmount] = useState("")

  const [transactions, setTransactions] = useState([])

  async function loadUser(currentToken) {

    try {

      const balanceRes = await axios.get(
        `${API}/balance/admin`,
        {
          headers: {
            Authorization: `Bearer ${currentToken}`
          }
        }
      )

      const txRes = await axios.get(
        `${API}/transactions`,
        {
          headers: {
            Authorization: `Bearer ${currentToken}`
          }
        }
      )

      setUser(balanceRes.data)
      setTransactions(txRes.data)

    } catch (err) {
      console.log(err)
    }
  }

  useEffect(() => {

    if (token) {
      loadUser(token)
    }

  }, [token])

  async function login() {

    try {

      const res = await axios.post(`${API}/login`, {
        username,
        password
      })

      localStorage.setItem("token", res.data.token)

      setToken(res.data.token)

    } catch (err) {

      alert("Erro no login")
    }
  }

  async function transfer() {

    try {

      await axios.post(
        `${API}/transfer`,
        {
          to_user: receiver,
          amount: parseFloat(amount)
        },
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      )

      setReceiver("")
      setAmount("")

      await loadUser(token)

      alert("Transferência enviada")

    } catch (err) {

      alert("Erro na transferência")
    }
  }

  function logout() {

    localStorage.removeItem("token")

    setToken("")
    setUser(null)
    setTransactions([])
  }

  if (!token || !user) {

    return (

      <div style={{
        background:"#050014",
        minHeight:"100vh",
        padding:"30px",
        color:"white"
      }}>

        <div style={{
          background:"#2d1170",
          padding:"40px",
          borderRadius:"25px",
          marginTop:"150px"
        }}>

          <h2>Login</h2>

          <input
            placeholder="Username"
            value={username}
            onChange={(e)=>setUsername(e.target.value)}
            style={input}
          />

          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e)=>setPassword(e.target.value)}
            style={input}
          />

          <button
            onClick={login}
            style={button}
          >
            Entrar
          </button>

        </div>

      </div>
    )
  }

  return (

    <div style={{
      background:"#050014",
      minHeight:"100vh",
      padding:"30px",
      color:"white"
    }}>

      <div style={card}>
        <h2>NUVIBANK™</h2>
        <p>Sistema fintech operacional.</p>
      </div>

      <div style={card}>
        <h2>{user.username}</h2>

        <h1 style={{
          color:"#00d9ff",
          fontSize:"72px"
        }}>
          ${user.balance}
        </h1>

        <button
          onClick={logout}
          style={{
            ...button,
            width:"200px",
            background:"#ff2b5f"
          }}
        >
          Logout
        </button>
      </div>

      <div style={card}>

        <h2>Transferência</h2>

        <input
          placeholder="Destinatário"
          value={receiver}
          onChange={(e)=>setReceiver(e.target.value)}
          style={input}
        />

        <input
          placeholder="Valor"
          value={amount}
          onChange={(e)=>setAmount(e.target.value)}
          style={input}
        />

        <button
          onClick={transfer}
          style={button}
        >
          Enviar
        </button>

      </div>

      <div style={card}>

        <h2>Histórico</h2>

        {

          transactions.map((tx, index)=>(

            <div
              key={index}
              style={{
                marginTop:"15px",
                padding:"15px",
                background:"#17003d",
                borderRadius:"15px"
              }}
            >
              {tx.from_user} → {tx.to_user} : ${tx.amount}
            </div>

          ))
        }

      </div>

    </div>
  )
}

const card = {
  background:"#2d1170",
  padding:"40px",
  borderRadius:"25px",
  marginBottom:"30px"
}

const input = {
  width:"100%",
  padding:"20px",
  marginTop:"20px",
  borderRadius:"15px",
  border:"none",
  background:"#17003d",
  color:"white",
  fontSize:"24px",
  boxSizing:"border-box"
}

const button = {
  width:"100%",
  padding:"20px",
  marginTop:"20px",
  border:"none",
  borderRadius:"20px",
  background:"linear-gradient(90deg,#ff2b8a,#00d9ff)",
  color:"white",
  fontSize:"32px",
  fontWeight:"bold"
}

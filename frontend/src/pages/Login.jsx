import { useState } from "react"
import axios from "axios"

export default function Login({ setToken, setUser }) {

  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")

  async function login() {

    try {

      const res = await axios.post(
        "http://10.142.231.104:5000/login",
        {
          username,
          password
        }
      )

      localStorage.setItem("token", res.data.token)
      localStorage.setItem("user", res.data.user)

      setToken(res.data.token)
      setUser(res.data.user)

    } catch (err) {

      console.log(err)

      alert("Erro no login")
    }
  }

  return (
    <div
      style={{
        minHeight: "100vh",
        background: "#050014",
        display: "flex",
        justifyContent: "center",
        alignItems: "center"
      }}
    >
      <div
        style={{
          width: "90%",
          maxWidth: 400,
          background: "#2c0b73",
          padding: 30,
          borderRadius: 20
        }}
      >

        <h2 style={{ color: "white" }}>
          Login
        </h2>

        <input
          placeholder="Username"
          value={username}
          onChange={(e) =>
            setUsername(e.target.value)
          }
          style={{
            width: "100%",
            padding: 20,
            marginTop: 20,
            borderRadius: 15,
            border: "none",
            background: "#18003f",
            color: "white",
            fontSize: 20
          }}
        />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) =>
            setPassword(e.target.value)
          }
          style={{
            width: "100%",
            padding: 20,
            marginTop: 20,
            borderRadius: 15,
            border: "none",
            background: "#18003f",
            color: "white",
            fontSize: 20
          }}
        />

        <button
          onClick={login}
          style={{
            width: "100%",
            padding: 20,
            marginTop: 20,
            borderRadius: 15,
            border: "none",
            background:
              "linear-gradient(90deg,#ff2079,#00d4ff)",
            color: "white",
            fontSize: 22,
            fontWeight: "bold"
          }}
        >
          Entrar
        </button>

      </div>
    </div>
  )
}

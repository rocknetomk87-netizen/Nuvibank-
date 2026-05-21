import { motion } from "framer-motion";
import { useContext } from "react";
import { AuthContext } from "../context/AuthContext";

export default function Dashboard() {
  const { user, logout } = useContext(AuthContext);

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="space-y-6"
    >
      <div className="bg-[#24126A] rounded-3xl p-6">
        <h1 className="text-4xl font-bold">
          NUVIBANK™
        </h1>

        <p className="text-zinc-300 mt-2">
          Sistema fintech operacional.
        </p>
      </div>

      <div className="bg-[#24126A] rounded-3xl p-6">
        <h2 className="text-2xl font-bold">
          Utilizador
        </h2>

        <p className="text-cyan-400 mt-2">
          {user || "Não autenticado"}
        </p>

        <button
          onClick={logout}
          className="mt-4 px-6 py-3 rounded-xl bg-red-500 font-bold"
        >
          Logout
        </button>
      </div>

      <div className="bg-[#24126A] rounded-3xl p-6">
        <h2 className="text-2xl font-bold">
          Segurança
        </h2>

        <p className="text-zinc-300 mt-2">
          JWT + bcrypt + React Context.
        </p>
      </div>
    </motion.div>
  );
}

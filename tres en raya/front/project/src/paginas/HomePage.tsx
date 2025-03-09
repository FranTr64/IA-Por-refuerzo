import { useState, useEffect } from "react";

export default function HomePage() {
  const [Idy, setIdy] = useState(0);
  const [game_over, setGame_over] = useState(false);
  const [rondas_max, setRondas_max] = useState(-1);
  const [rondas, setRondas] = useState(-5);
  const [puntuacion, setPuntuacion] = useState([]);
  const [numero, setNumero] = useState(0);
  const [tablero, setTablero] = useState([
    ["", "", ""],
    ["", "", ""],
    ["", "", ""],
  ]);
  const [nombre_1, setNombre_1] = useState("");
  const [nombre_2, setNombre_2] = useState("");
  const [ganador, setGanador] = useState("");

  var clase_bloque = "flex";
  var clase_recuadro =
    "flex bg-sky-900 size-28 m-2 justify-center items-center border-8 border-white rounded-xl";

  var victoria = "blinking";

  function Juego(datos) {
    try {
      setPuntuacion(datos["puntuacion"]);
      setRondas_max(datos["rondas maximas"]);
      setRondas(datos["rondas jugadas"]);
      setGame_over(datos["game over"]);
      setIdy(datos["Id"]);
      setNombre_1(datos["Jugador_1"]);
      setNombre_2(datos["Jugador_2"]);
      setGanador(datos["Ganador"]);
      const tablero = datos["tablero"];
      var forma = [
        ["", "", ""],
        ["", "", ""],
        ["", "", ""],
      ];
      for (let i = 0; i < 3; i++) {
        for (let j = 0; j < 3; j++) {
          if (tablero[i][j] == 1) {
            forma[i][j] = "X";
          } else if (tablero[i][j] == -1) {
            forma[i][j] = "O";
          }
        }
      }
      setTablero(forma);
      if (datos["game over"]) {
        Fin_Juego(datos);
      }
    } catch {
      console.log("La funcion juego da el error");
    }
  }
  useEffect(() => {
    document.getElementById("Juego").classList.add("hidden");
    document.getElementById("Opciones").classList.remove("hidden");
  }, []);
  function ReIniciar() {
    let j1 = document.getElementById("j1").children;
    let j2 = document.getElementById("j2").children;
    for (let i = 0; i < j1.length; i++) {
      j1[i].classList.remove("clases_ganador");
    }
    for (let i = 0; i < j2.length; i++) {
      j2[i].classList.remove("clases_ganador");
    }
    let b2 = document.getElementById("Boton_Inicio");
    b2.classList.add("hidden");
    document.getElementById("Juego").classList.add("hidden");
    document.getElementById("Opciones").classList.remove("hidden");
  }
  function Fin_Juego(datos) {
    let tableta = document.getElementById("tablero_tres");
    tableta.classList.add("blinking");
    if (rondas >= rondas_max) {
      let boton2 = document.getElementById("Boton_Inicio");
      boton2.classList.remove("hidden");
    } else {
      document.getElementById("Boton_Restart")?.classList.remove("hidden");
    }
    if (datos["Ganador"] == "1") {
      let j_ganador = document.getElementById("j1").children;
      for (let i = 0; i < j_ganador.length; i++) {
        j_ganador[i].classList.add("clases_ganador");
      }
    } else if (datos["Ganador"] == "-1") {
      let j_ganador = document.getElementById("j2").children;
      for (let i = 0; i < j_ganador.length; i++) {
        j_ganador[i].classList.add("clases_ganador");
      }
    }
  }
  function Eleccion(eleccion) {
    const numero_bueno = Math.round(numero);
    const data = {
      primero: eleccion,
      rondas_max: numero_bueno,
    };
    if (numero_bueno > 0) {
      fetch("http://localhost:8000/iniciar_partida/", {
        method: "POST",
        credentials: "include",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCookie(),
        },
        body: JSON.stringify(data),
      })
        .then((response) => {
          if (!response.ok) {
            console.log(response);
            throw new Error(
              "Error, no se ha podido hace el fetch correctamente. Este fetch es el de la eleccion."
            );
          }
          return response.json();
        })
        .then((datos) => {
          Juego(datos);
          document.getElementById("Opciones").classList.add("hidden");
          document.getElementById("Juego").classList.remove("hidden");
          document.getElementById("tablero_tres").classList.remove("blinking");
        })
        .catch((error) => {
          console.error("[Algo fue mal con la eleccion. ¡Busca el error!]");
          console.error(error);
        });
    } else {
      alert("Introduce un numero de rondas a jugar");
    }
  }

  function Restart() {
    let j1 = document.getElementById("j1").children;
    let j2 = document.getElementById("j2").children;
    for (let i = 0; i < j1.length; i++) {
      j1[i].classList.remove("clases_ganador");
    }
    for (let i = 0; i < j2.length; i++) {
      j2[i].classList.remove("clases_ganador");
    }
    document.getElementById("Boton_Restart")?.classList.add("hidden");
    let tableta = document.getElementById("tablero_tres");
    tableta.classList.remove("blinking");
    fetch("http://localhost:8000/reset_partida/", {
      method: "POST",
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie(),
      },
      body: JSON.stringify({ id: Idy }),
    })
      .then((response) => {
        if (!response.ok) {
          console.log(response);
          throw new Error(
            "Error, no se ha podido hace el fetch correctamente. Este fetch es el del reinicio."
          );
        }
        return response.json();
      })
      .then((datos) => {
        Juego(datos);
      })
      .catch((error) => {
        console.error("[Algo fue mal con el reinicio. ¡Busca el error!]");
        console.error(error);
      });
  }
  function getCookie() {
    const cookie = document.cookie
      .split("; ")
      .find((row) => row.startsWith("csrftoken"))
      .split("=")[1];
    return cookie;
  }
  const Movimiento = (num1, num2) => {
    if (tablero[num1][num2] == '') {
      const data = {
        id: Idy,
        mov_1: num1,
        mov_2: num2,
      };
      fetch("http://localhost:8000/realizar_jugada/", {
        method: "POST",
        credentials: "include",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCookie(),
        },
        body: JSON.stringify(data),
      })
        .then((response) => {
          if (!response.ok) {
            console.log(response);
            throw new Error(
              "Error, no se ha podido hace el fetch correctamente"
            );
          }
          return response.json();
        })
        .then((datos) => {
          Juego(datos);
        })
        .catch((error) => {
          console.error("[Algo fue mal. ¡Busca el error!]");
          console.error(error);
        });
    }
  };
  return (
    <div class="flex justify-center items-center w-full h-full">
      <div
        id="Opciones"
        class="w-1/4 h-1/2 flex flex-col justify-center items-center bg-white/60 rounded-2xl border-8 border-emerald-400"
      >
        <p class="text-center mb-5 text-3xl font-medium">¿Que prefieres?</p>
        <div class="flex justify-around items-center w-5/6 m-7 text-xl">
          <button class="size-16" onClick={() => Eleccion(true)}>
            X
          </button>
          <button class="size-16" onClick={() => Eleccion(false)}>
            O
          </button>
        </div>
        <input
          class="w-3/4 text-center"
          type="number"
          onChange={(e) => setNumero(Number(e.target.value))}
          placeholder="¿Numero de rondas a jugar?"
        />
        <p class="text-center mt-10">Nota: Siempre empiezan las X</p>
      </div>
      <div
        id="Juego"
        class="flex flex-col justify-center items-center w-1/2 hidden"
      >
        <div class="flex w-full justify-between items-center m-4">
          <div
            id="j1"
            class="flex justify-center items-center w-1/4 text-lg font-medium"
          >
            <p class="mr-2">{nombre_1}</p>
            <p>{puntuacion[0]}</p>
          </div>
          <div class="flex justify-center items-center w-1/2">
            <button id="Boton_Restart" class="hidden" onClick={() => Restart()}>
              Siguiente Ronda
            </button>
            <button
              id="Boton_Inicio"
              class="hidden"
              onClick={() => ReIniciar()}
            >
              Comenzar de nuevo
            </button>
          </div>
          <div
            id="j2"
            class="flex justify-center items-center w-1/4 text-lg font-medium"
          >
            <p>{puntuacion[1]}</p>
            <p class="ml-2">{nombre_2}</p>
          </div>
        </div>
        <div
          id="tablero_tres"
          class="w-auto bg-blue-950 text-white text-7xl p-4 justify-center items-center rounded-xl"
        >
          <div class={`${clase_bloque}`}>
            <div id="00" class={`${clase_recuadro}`}>
              <button
                class="w-full h-full rounded-none bg-transparent p-0 border-0"
                onClick={() => Movimiento(0, 0)}
              >
                {tablero[0][0]}
              </button>
            </div>
            <div id="01" class={`${clase_recuadro}`}>
              <button
                class="w-full h-full rounded-none bg-transparent p-0 border-0"
                onClick={() => Movimiento(0, 1)}
              >
                {tablero[0][1]}
              </button>
            </div>
            <div id="02" class={`${clase_recuadro}`}>
              <button
                class="w-full h-full rounded-none bg-transparent p-0 border-0"
                onClick={() => Movimiento(0, 2)}
              >
                {tablero[0][2]}
              </button>
            </div>
          </div>
          <div class={`${clase_bloque}`}>
            <div id="10" class={`${clase_recuadro}`}>
              <button
                class="w-full h-full rounded-none bg-transparent p-0 border-0"
                onClick={() => Movimiento(1, 0)}
              >
                {tablero[1][0]}
              </button>
            </div>
            <div id="11" class={`${clase_recuadro}`}>
              <button
                class="w-full h-full rounded-none bg-transparent p-0 border-0"
                onClick={() => Movimiento(1, 1)}
              >
                {tablero[1][1]}
              </button>
            </div>
            <div id="12" class={`${clase_recuadro}`}>
              <button
                class="w-full h-full rounded-none bg-transparent p-0 border-0"
                onClick={() => Movimiento(1, 2)}
              >
                {tablero[1][2]}
              </button>
            </div>
          </div>
          <div class={`${clase_bloque}`}>
            <div id="20" class={`${clase_recuadro}`}>
              <button
                class="w-full h-full rounded-none bg-transparent p-0 border-0"
                onClick={() => Movimiento(2, 0)}
              >
                {tablero[2][0]}
              </button>
            </div>
            <div id="21" class={`${clase_recuadro}`}>
              <button
                class="w-full h-full rounded-none bg-transparent p-0 border-0"
                onClick={() => Movimiento(2, 1)}
              >
                {tablero[2][1]}
              </button>
            </div>
            <div id="22" class={`${clase_recuadro}`}>
              <button
                class="w-full h-full rounded-none bg-transparent p-0 border-0"
                onClick={() => Movimiento(2, 2)}
              >
                {tablero[2][2]}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

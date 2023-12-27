const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors')

const app = express();
const PORT = 3000;

const KAE = "e0b045";
const KAF = "e0b046";
const KAFf = "KAFf";
const KAEf = "KAEf";

app.use(cors())

let jsonData = null;
let vuelosGuardados = {};

// Middleware para analizar el cuerpo de las solicitudes JSON
app.use(bodyParser.json());


// Ruta para recibir el JSON por GET
app.get('/vuelos', (req, res) => {
  if (jsonData) {
    if (!jsonData.hasOwnProperty(KAE) && vuelosGuardados.hasOwnProperty(KAEf)){
      jsonData[KAEf] = vuelosGuardados[KAEf];
      //jsonData["pepeE"] = vuelosGuardados[KAE];
    }
    if (!jsonData.hasOwnProperty(KAF) && vuelosGuardados.hasOwnProperty(KAFf)){
      jsonData[KAFf] = vuelosGuardados[KAFf];
      //jsonData["pepeF"] = [0,1,2,3];
    }

    res.json(jsonData);
  } else {
    res.status(404).json('sin datos');
  }
});

// Ruta para enviar el JSON por POST y almacenarlo en memoria
app.post('/vuelos', (req, res) => {
    //jsonData = null;
    jsonData = req.body;

    if (jsonData.hasOwnProperty(KAE)){
      jsonData[KAE].push(new Date());
      //vuelosGuardados.KAEf = [...jsonData[KAE]];
      vuelosGuardados.KAEf = [...jsonData[KAE]];
      console.log("KAE presente");
    }
    if (jsonData.hasOwnProperty(KAF)){
      jsonData[KAF].push(new Date());
      vuelosGuardados.KAFf = [...jsonData[KAF]];
      console.log("KAF presente");
    }
    for (let key in jsonData) {
      if (
        jsonData.hasOwnProperty(key) &&
        Array.isArray(jsonData[key]) &&
        (jsonData[key][1] === 0 || jsonData[key][2] === 0)
      ) {
        delete jsonData[key];
      }
    }

    console.log("cantidad de vuelos en seguimiento " + Object.keys(jsonData).length);
    res.json({ message: 'Datos recibidos y almacenados en memoria' });
});

// Inicia el servidor
app.listen(PORT, () => {
  console.log(`Servidor escuchando en http://x.x.x.x:${PORT}`);
});

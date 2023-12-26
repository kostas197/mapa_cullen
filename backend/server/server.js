const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors')

const app = express();
const PORT = 3000;
app.use(cors())

let jsonData = null;

// Middleware para analizar el cuerpo de las solicitudes JSON
app.use(bodyParser.json());


// Ruta para recibir el JSON por GET
app.get('/vuelos', (req, res) => {
  if (jsonData) {
    res.json(jsonData);
  } else {
    res.status(404).json('sin datos');
  }
});

// Ruta para enviar el JSON por POST y almacenarlo en memoria
app.post('/vuelos', (req, res) => {
    jsonData = req.body;

    //var KAE = "e0b045";
    var KAE = "a12d2f";
    var KAF = "e0b046";

    if (jsonData.hasOwnProperty(KAE)){
        datosKAE = [];
        datosKAE = jsonData[KAE];
        datosKAE[17] = new Date();
        jsonData['LVKAEf'] = jsonData[KAE];
        //console.log(jsonData['LVKAEf']);
    }
    if (jsonData.hasOwnProperty(KAF)){
        datosKAE = [];
        datosKAE = jsonData[KAF];
        datosKAE[17] = new Date();
        jsonData['LVKAFf'] = jsonData[KAF];
        //console.log(jsonData['LVKAFf']);
    }
    console.log(jsonData)
    res.json({ message: 'Datos recibidos y almacenados en memoria' });
});

// Inicia el servidor
app.listen(PORT, () => {
  console.log(`Servidor escuchando en http://x.x.x.x:${PORT}`);
});

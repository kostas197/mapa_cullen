# Cullen Flight Map / MapaCullen

## English

This project displays a real-time map of airplane traffic near Bernal Este, Buenos Aires, Argentina. The data is captured by a personal ADS-B receiver.

### Project Evolution

This project began as a simple flight plotter using a tech stack of Bash scripts, Node.js, and a frontend built with HTML and jQuery.

The codebase has since been significantly modernized and refactored. The current version features:

- A **Python backend** (using Flask) to process the flight data.
- Full containerization with **Docker and Docker Compose** for easy deployment.
- A **Cloudflare Tunnel** to securely expose the service to the internet.
- Various other improvements to enhance stability and performance.

### Hardware Setup

The flight data is received using a **Raspberry Pi 2** connected to an **RTL-SDR** dongle. The receiver uses a small antenna located on the third floor of a building.

### Live Demo

You can view the live flight map at: **https://vuelos.kmc.ar**

Despite the modest hardware setup, the receiver often picks up signals from aircraft over Uruguay, demonstrating its good range.

About the name of the proyect, It's the name of my previous job location. Cullen, Tierra del Fuego, Argentina.

---

## Español

Este proyecto muestra un mapa en tiempo real del tráfico aéreo cerca de Bernal Este, Buenos Aires, Argentina. Los datos son capturados por un receptor ADS-B personal.

### Evolución del Proyecto

Este proyecto comenzó como un simple ploteador de vuelos que usaba un stack tecnológico de scripts de Bash, Node.js y un frontend hecho con HTML y jQuery.

Desde entonces, el código ha sido modernizado y refactorizado significativamente. La versión actual incluye:

- Un **backend en Python** (usando Flask) para procesar los datos de los vuelos.
- Contenerización completa con **Docker y Docker Compose** para un despliegue sencillo.
- Un **Túnel de Cloudflare** para exponer el servicio de forma segura a internet.
- Otras varias mejoras para aumentar la estabilidad y el rendimiento.

### Configuración del Hardware

Los datos de los vuelos se reciben usando una **Raspberry Pi 2** conectada a un dongle **RTL-SDR**. El receptor utiliza una pequeña antena ubicada en un tercer piso.

### Demo en Vivo

Puedes ver el mapa de vuelos en tiempo real en: **https://vuelos.kmc.ar**

A pesar de la modesta configuración del hardware, el receptor a menudo capta señales de aeronaves sobre Uruguay, demostrando su buen alcance.

Sobre el nombre del proyecto. MapaCullen, este es el nombre de mi lugar de trabajo, el mismo se encuentra en Cullen, Tierra del Fuego, Argentina.

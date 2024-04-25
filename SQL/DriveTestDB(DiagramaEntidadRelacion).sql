SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS `Preguntas`;
DROP TABLE IF EXISTS `Respuestas`;
DROP TABLE IF EXISTS `Estudiante`;
DROP TABLE IF EXISTS `Examen`;
DROP TABLE IF EXISTS `HistorialEstudiante`;
DROP TABLE IF EXISTS `Imagenes`;
SET FOREIGN_KEY_CHECKS = 1;

CREATE TABLE `Preguntas` (
    `preguntaId` INTEGER NOT NULL,
    `imagenId` INTEGER NOT NULL,
    `reactivo` VARCHAR(200) NOT NULL,
    PRIMARY KEY (`preguntaId`)
);

CREATE TABLE `Respuestas` (
    `respuestasId` INTEGER NOT NULL,
    `preguntaId` INTEGER NOT NULL,
    `opcion` VARCHAR(200) NOT NULL,
    `tipo` BOOLEAN NOT NULL,
    PRIMARY KEY (`respuestasId`)
);

CREATE TABLE `Estudiante` (
    `matricula` VARCHAR(9) NOT NULL,
    `nombre` VARCHAR(50) NOT NULL,
    `apellidoPaterno` VARCHAR(50) NOT NULL,
    `apellidoMaterno` VARCHAR(50) NOT NULL,
    `email` VARCHAR(50) NOT NULL,
    `telefono` BIGINT NOT NULL,
    `calificacionFinal` DOUBLE NOT NULL,
    PRIMARY KEY (`matricula`)
);

CREATE TABLE `Examen` (
    `examenId` INTEGER NOT NULL,
    `matricula` VARCHAR(9) NOT NULL,
    `preguntaId` INTEGER NOT NULL,
    `respuestaId` INTEGER NOT NULL,
    PRIMARY KEY (`examenId`)
);

CREATE TABLE `HistorialEstudiante` (
    `HistorialEstudiante` INTEGER NOT NULL,
    `matricula` VARCHAR(9) NOT NULL,
    `fechaRealizacion` DATETIME NOT NULL,
    `tipo` VARCHAR(50) NOT NULL,
    `calificacion` DOUBLE NOT NULL,
    PRIMARY KEY (`HistorialEstudiante`)
);

CREATE TABLE `Imagenes` (
    `imagenId` INTEGER NOT NULL,
    `ruta` VARCHAR(200) NOT NULL,
    PRIMARY KEY (`imagenId`)
);

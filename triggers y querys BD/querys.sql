-- Querys para tipo reserva y estado reserva --

INSERT INTO `app_estadoreserva` (`estadoReservaId`, `estadoReservaNombre`) VALUES ('1', 'Guardado');
INSERT INTO `app_estadoreserva` (`estadoReservaId`, `estadoReservaNombre`) VALUES ('2', 'Anulado');
INSERT INTO `app_estadoreserva` (`estadoReservaId`, `estadoReservaNombre`) VALUES ('3', 'Confirmado');


INSERT INTO `app_tiporeserva` (`tipoSolicitudId`, `tipoSolicitud`) VALUES ('1', 'JR Suite');
INSERT INTO `app_tiporeserva` (`tipoSolicitudId`, `tipoSolicitud`) VALUES ('2', 'PentHouse');
INSERT INTO `app_tiporeserva` (`tipoSolicitudId`, `tipoSolicitud`) VALUES ('3', 'Habitacion tematica');

-- Query de reserva Francisco Aurelio --

INSERT INTO `app_reserva` (`idSolicitud`, `nombre`, `telefono`, `fechaNacimiento`, `fechareserva`, `horareserva`, `cantidadHermanos`, `observaciones`, `website`, `email`, `donante`, `imagenCarnet`, `F_Creacion`, `F_Modificacion`, `estadoReservaId_id`, `tipoSolicitudId_id`) VALUES (1, 'Fran', '977267217', '1993-07-05', '2023-11-27', '08:40:00.000000', 5, 'hoy no hay observaciones ni mucho menos', 'https://www.bancofalabella.cl/BancoFalabellaChile/index.html', 'sanchezcamposfrancisco@gmail.com', 0, 'media/perfilpicnigga.png', '2023-11-20 23:33:38.000000', '2023-11-20 23:33:38.000000', '1', '2');

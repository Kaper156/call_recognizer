create table project
(
    id          serial not null
        constraint project_pkey
            primary key,
    name        varchar(256),
    description text
);

alter table project
    owner to postgres;

INSERT INTO public.project (id, name, description)
VALUES (1, 'TestProject', null);
INSERT INTO public.project (id, name, description)
VALUES (2, 'Тестовый проект#2', null);
INSERT INTO public.project (id, name, description)
VALUES (3, 'Тестовый проект №1', null);


create table server
(
    id          serial not null
        constraint server_pkey
            primary key,
    name        varchar(256),
    ip_address  inet,
    description text
);

alter table server
    owner to postgres;

INSERT INTO public.server (id, name, ip_address, description)
VALUES (1, 'TestServer', '8.8.8.8', null);
INSERT INTO public.server (id, name, ip_address, description)
VALUES (2, 'Тестовый сервер#2', '127.0.0.1', null);
INSERT INTO public.server (id, name, ip_address, description)
VALUES (3, 'Тестовый сервер №1', '1.1.1.1', null);

create table phone_call
(
    id            serial not null
        constraint phone_call_pkey
            primary key,
    date          date,
    time          time,
    phone_number  bigint,
    duration      double precision,
    transcription text,
    stages        integer,
    count_stages  smallint,
    project_id    integer
        constraint phone_call_project_id_fkey
            references project,
    server_id     integer
        constraint phone_call_server_id_fkey
            references server
);

alter table phone_call
    owner to postgres;

INSERT INTO public.phone_call (id, date, time, phone_number, duration, transcription, stages, count_stages, project_id,
                               server_id)
VALUES (2, '2020-08-27', '12:45:21', 8904123456, 5.7, 'вас приветствует автоответчик оставьте сообщение после сигнала',
        0, 1, 1, 1);
INSERT INTO public.phone_call (id, date, time, phone_number, duration, transcription, stages, count_stages, project_id,
                               server_id)
VALUES (3, '2020-08-27', '13:26:11', 8904654321, 3.3, 'алло говорите', 3, 2, 1, 1);
INSERT INTO public.phone_call (id, date, time, phone_number, duration, transcription, stages, count_stages, project_id,
                               server_id)
VALUES (4, '2020-08-27', '14:15:31', 8904654123, 4.5, 'ну да удобно его слушаю', 3, 2, 1, 1);
INSERT INTO public.phone_call (id, date, time, phone_number, duration, transcription, stages, count_stages, project_id,
                               server_id)
VALUES (5, '2020-08-27', '15:32:21', 8904456123, 3.9, 'нет я сейчас на работе до свидания', 1, 2, 1, 1);
INSERT INTO public.phone_call (id, date, time, phone_number, duration, transcription, stages, count_stages, project_id,
                               server_id)
VALUES (6, '2020-08-27', '22:41:21', 8956123456, 5.7, 'вас приветствует автоответчик оставьте сообщение после сигнала',
        0, 1, 2, 2);
INSERT INTO public.phone_call (id, date, time, phone_number, duration, transcription, stages, count_stages, project_id,
                               server_id)
VALUES (7, '2020-08-27', '23:21:11', 8956654321, 3.3, 'алло говорите', 3, 2, 2, 2);
INSERT INTO public.phone_call (id, date, time, phone_number, duration, transcription, stages, count_stages, project_id,
                               server_id)
VALUES (8, '2020-08-27', '20:11:31', 8956654123, 4.5, 'ну да удобно его слушаю', 3, 2, 2, 2);
INSERT INTO public.phone_call (id, date, time, phone_number, duration, transcription, stages, count_stages, project_id,
                               server_id)
VALUES (9, '2020-08-27', '21:31:21', 8956456123, 3.9, 'нет я сейчас на работе до свидания', 1, 2, 2, 2);
INSERT INTO public.phone_call (id, date, time, phone_number, duration, transcription, stages, count_stages, project_id,
                               server_id)
VALUES (10, '2020-08-27', '22:42:21', 8937123456, 5.7, 'вас приветствует автоответчик оставьте сообщение после сигнала',
        0, 1, 3, 3);
INSERT INTO public.phone_call (id, date, time, phone_number, duration, transcription, stages, count_stages, project_id,
                               server_id)
VALUES (11, '2020-08-27', '23:22:11', 8937654321, 3.3, 'алло говорите', 3, 2, 3, 3);
INSERT INTO public.phone_call (id, date, time, phone_number, duration, transcription, stages, count_stages, project_id,
                               server_id)
VALUES (12, '2020-08-27', '20:12:31', 8937654123, 4.5, 'ну да удобно его слушаю', 3, 2, 3, 3);
INSERT INTO public.phone_call (id, date, time, phone_number, duration, transcription, stages, count_stages, project_id,
                               server_id)
VALUES (13, '2020-08-27', '21:32:21', 8937456123, 3.9, 'нет я сейчас на работе до свидания', 1, 2, 3, 3);
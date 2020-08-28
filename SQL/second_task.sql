CREATE OR REPLACE FUNCTION second_task(_date_from date, _date_to date DEFAULT NULL)
    RETURNS TABLE
            (
                date           date,
                is_human       boolean,
                is_comfort     boolean,
                count          bigint,
                server         varchar(256),
                project        varchar(256),
                total_duration double precision
            )
AS
$func$
BEGIN

    RETURN QUERY
        SELECT pc.date           as "date",
               pc.stages & 1 > 0 as "is_human", -- Use mask to get concrete answer
               pc.stages & 2 > 0 as "is_comfort",
               count(pc.stages)  as "count",
               p.name            as "server",
               s.name            as "project",
               sum(pc.duration)  as "total_duration"
        FROM phone_call as pc
                 INNER JOIN project p on pc.project_id = p.id
                 INNER JOIN server s on pc.server_id = s.id
        WHERE pc.date >= _date_from
          and pc.date < COALESCE(_date_to, _date_from + '1 day'::interval)
        GROUP BY pc.date, "is_human", "is_comfort", p.id, s.id
        ORDER BY pc.date;

END
$func$ LANGUAGE plpgsql;

SELECT *
FROM second_task('2020-08-26'::date);

SELECT *
FROM second_task('2020-08-27'::date);

SELECT *
FROM second_task('2020-08-25'::date, '2020-08-30'::date);

-- P.S. To filter phone calls by many answers just use bit mask, like:
-- pc.stages & 3 > 0  [0b11](Correct talk client ready to advertise)
-- pc.stages & 1 > 0  [0b1] (Got answerphone)
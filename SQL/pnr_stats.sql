create table IF NOT EXISTS PNR_STATS
(
	id serial,
	pnr bigint,
	query_date bigint default extract(epoch from now())::int
)

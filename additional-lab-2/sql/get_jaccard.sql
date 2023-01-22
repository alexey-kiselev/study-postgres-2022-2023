WITH k_list AS
(
    SELECT 2 AS "k"
    UNION ALL
    SELECT 5 AS "k"
    UNION ALL
    SELECT 9 AS "k"
)
SELECT
    k_list.k AS "k",
    (
        (SELECT COUNT(*) FROM (
            SELECT DISTINCT element
            FROM additional.genome_sequense
            WHERE genome = 'A' AND k = k_list.k
            INTERSECT
            SELECT DISTINCT element
            FROM additional.genome_sequense
            WHERE genome = 'B' AND k = k_list.k
        ) AS genomes_intersect)::decimal
        /
        (SELECT COUNT(*) FROM (
            SELECT DISTINCT element
            FROM additional.genome_sequense
            WHERE genome = 'A' AND k = k_list.k
            UNION
            SELECT DISTINCT element
            FROM additional.genome_sequense
            WHERE genome = 'B' AND k = k_list.k
        ) AS genomes_union)::decimal
    ) AS "J"
FROM k_list
ORDER BY k_list.k;

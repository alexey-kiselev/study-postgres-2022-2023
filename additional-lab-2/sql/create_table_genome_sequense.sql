CREATE SCHEMA IF NOT EXISTS additional;

CREATE TABLE additional.genome_sequense
(
    genome VARCHAR(20),
    k INT CHECK(k>=2),
    index INT CHECK(index>=0),
    element VARCHAR CHECK(length(element) = k),
    
    PRIMARY KEY (genome, k, index)
);

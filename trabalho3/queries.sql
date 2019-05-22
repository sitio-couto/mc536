
-- OP1 - Recupera (cpf,nome,email) dos integrantes da Faculdade Estadual da Bahia
SELECT p.cpf, p.nome, p.email
FROM InstituicaoAcademica AS ia INNER JOIN Pessoa AS p
ON ia.cnpj = p.cnpj
WHERE ia.nome = 'Universidade Estadual de Belém';

-- OP2 - Recupera o id de toda questao sobre Cálculo (id=1)
SELECT id_questao
FROM Aborda
WHERE id_materia = 1;

-- -- Pegar com enunciado para mostra que realmete são de cálculo
-- SELECT Questao.enunciado, Questao.id
-- FROM Questao INNER JOIN Aborda
-- ON Questao.id = Aborda.id_questao
-- WHERE id_materia = 1;

-- OP3 - Lista enunciados das questões da Olimpíada Brasileira de Matemática Avançada nivel 22 (id=1)
SELECT Questao.enunciado
FROM Questao INNER JOIN Compoe
ON Questao.id = Compoe.id_questao
WHERE Compoe.id_prova = 1;

-- OP4 - Lista cpf de todos que fizeram a Olimpíada Brasileira de Biologia nivel 9 (id=10)
--       e sao integrantes da Universidade Estadual de Belém
SELECT p.cpf
FROM Pessoa AS p INNER JOIN InstituicaoAcademica AS ia
ON ia.nome = 'Universidade Estadual de Belém' AND ia.cnpj = p.cnpj
INNER JOIN Realiza AS r
ON r.id_prova = 10 AND p.cpf = r.cpf;

-- OBS: Para demostrar a restição do domínio na OP4
-- -- Apenas integrantes da Universidade Estadual de Belém
-- SELECT p.cpf, p.nome
-- FROM Pessoa AS p INNER JOIN InstituicaoAcademica AS ia
-- ON ia.nome = 'Universidade Estadual de Belém' AND ia.cnpj = p.cnpj;
-- -- Apenas pessoas que fizeram a Olimpíada Internacional de Matemática nivel 5 (id=12)
-- SELECT p.cpf, p.nome
-- FROM Pessoa AS p INNER JOIN Realiza AS r
-- ON r.id_prova = 10 AND p.cpf = r.cpf;

-- OP5 - Lista todas as provas de nivel avançado (>=20)
SELECT *
FROM Prova
WHERE Prova.nivel >= 20;


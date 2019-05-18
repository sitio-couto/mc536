
-- OP1 - Recupera (cpf,nome,email) dos integrantes da Faculdade Estadual da Bahia
SELECT p.cpf, p.nome, p.email
FROM InstituicaoAcademica AS ia INNER JOIN Pessoa AS p
ON ia.cnpj = p.cnpj
WHERE ia.nome = 'Faculdade Estadual da Bahia';

-- OP2 - Recupera o id de toda questao sobre Cálculo (id=1)
SELECT id_questao
FROM Aborda
WHERE id_materia = 1;

-- OP3 - Lista enunciados das questões da Olimpíada Brasileira de Matemática Avançada (id=1)
SELECT Questao.enunciado
FROM Questao INNER JOIN Compoe
ON Questao.id = Compoe.id_questao
WHERE Compoe.id_prova = 1;

-- OP4 - Lista cpf de todos que fizeram a Competição Brasileira de Informática Básica (id=16)
--       e sao integrantes da Faculdade Estadual da Bahia
SELECT p.cpf
FROM Pessoa AS p INNER JOIN InstituicaoAcademica AS ia
ON ia.nome = 'Faculdade Estadual da Bahia' AND ia.cnpj = p.cnpj
INNER JOIN Realiza AS r
ON r.id_prova = 16 AND p.cpf = r.cpf;

-- -- OBS: Para demostrar a restição do domínio na OP4
-- -- Apenas integrantes da Faculdade Estadual da Bahia
-- SELECT p.nome
-- FROM Pessoa AS p INNER JOIN InstituicaoAcademica AS ia
-- ON ia.nome = 'Faculdade Estadual da Bahia' AND ia.cnpj = p.cnpj;
-- -- Apenas pessoas que fizeram a Competição Brasileira de Informática Básica (id=16)
-- SELECT p.nome
-- FROM Pessoa AS p INNER JOIN Realiza AS r
-- ON r.id_prova = 16 AND p.cpf = r.cpf;

-- OP5 - Lista todas as provas de dificuldade Avançada
SELECT *
FROM Prova
WHERE Prova.nivel = 'Avançada';


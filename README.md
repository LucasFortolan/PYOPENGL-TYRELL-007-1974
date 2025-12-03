# **Tyrrell 007 — Modelagem 3D em PyOpenGL**

Este projeto implementa uma cena 3D que apresenta o carro de Fórmula 1 **Tyrrell 007 (1974)** percorrendo uma pista infinita. O objetivo é aplicar conceitos fundamentais de computação gráfica utilizando **PyOpenGL** e **Pygame** para modelagem tridimensional, transformações geométricas, renderização e interação com o usuário.

---

## 🎯 **Objetivos do Projeto**
- Modelar o carro Tyrrell 007 utilizando **primitivas geométricas básicas**.
- Construir uma **pista infinita** com repetição procedural.
- Renderizar a cena usando **OpenGL**.
- Implementar **movimentação interativa** do carro e da câmera.
- Criar uma estrutura de código limpa e modular para aprendizagem.

---

## 🛠️ **Tecnologias Utilizadas**

### **Pygame**
Responsável por criar a janela, capturar eventos de teclado/mouse e desenhar textos na tela.

### **Pygame.locals**
Fornece constantes úteis para manipulação de eventos.

### **OpenGL.GL**
Contém as funções essenciais do OpenGL para desenhar primitivas, aplicar transformações e controlar a renderização.

### **OpenGL.GLU**
Possui funções utilitárias como configuração da câmera (`gluLookAt`) e perspectiva.

### **math**
Usada para trigonometria e cálculos matemáticos auxiliares nas animações e rotações.

---

## 🚗 **Processo de Modelagem**

O desenvolvimento iniciou-se analisando a estrutura do Tyrrell 007 original e traçando formas geométricas sobre sua imagem para identificar as primitivas necessárias. Essa decomposição visual permitiu planejar a modelagem 3D utilizando formas simples, como retângulos (formados pela união de dois triângulos).

Após essa etapa, cada parte do carro foi convertida para sua respectiva primitiva geométrica em PyOpenGL. A pista infinita foi criada através de blocos repetitivos que se deslocam continuamente, gerando a sensação de movimento constante.

---

## 🎮 **Controles do Usuário**

O código disponibiliza orientações diretamente na tela através do comando:

```python
desenhar_texto_na_tela(10, 10, [
    "Tyrrell 007 de 1974",
    f"Status: {status}",
    "Setas (Direção): <- Esquerda, -> Direita | R: Reset",
    "Mouse: Cam | Scroll: Zoom"
])

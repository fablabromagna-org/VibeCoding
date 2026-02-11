Perfetto.  
Ti preparo una versione **pulita, pronta da incollare in Obsidian**, coerente con le tue note tecniche.

---

# 📘 Filtro IIR (Media Esponenziale) – Appunto tecnico

## Definizione

Il filtro IIR (Infinite Impulse Response) implementa una **media esponenziale pesata**:

$$  
y_{filt} = (1 - \alpha), y_{prev} + \alpha, y_{new}  
$$

---

## Significato delle variabili

- $y_{new}$ → nuova misura (ADC, tensione, velocità, ecc.)
    
- $y_{prev}$ → valore filtrato precedente
    
- $\alpha$ → coefficiente di filtraggio $(0 < \alpha \le 1)$
    
- $y_{filt}$ → nuovo valore filtrato
    

---

## Interpretazione fisica

- $\alpha$ grande → sistema **reattivo**, poco filtrato
    
- $\alpha$ piccolo → sistema **stabile**, risposta lenta
    

Il filtro introduce una sorta di **inerzia digitale**, utile per:

- ridurre jitter ADC
    
- stabilizzare misure analogiche
    
- simulare comportamento fisico (es. vento)
    

---

## Esempio numerico

Valore precedente: $10$  
Nuova misura: $20$

Con $\alpha = 0.1$:

$$  
y = 0.9 \cdot 10 + 0.1 \cdot 20 = 11  
$$

Con $\alpha = 0.5$:

$$  
y = 0.5 \cdot 10 + 0.5 \cdot 20 = 15  
$$

---

## Scelta pratica di $\alpha$

|Applicazione|Valore consigliato|
|---|---|
|Demo LED reattiva|$0.2$ – $0.3$|
|Lettura stabile seriale|$0.1$ – $0.15$|
|Stazione meteo|$0.05$ – $0.1$|

---

## Nota ingegneristica

Il filtro IIR è equivalente a un **filtro passa-basso del primo ordine**.

La costante di tempo approssimativa è:

$$  
\tau \approx \frac{T_s}{\alpha}  
$$

dove:

- $T_s$ = tempo di campionamento
    
- $\tau$ = tempo caratteristico di risposta
    

---

"""
Capítulo 18 — O Espelho da Entrega
OCR de aceite de entrega + detecção de assinatura na linha.

PLUS:
  - Pipeline de pré-processamento documentado
  - Modo simulado (roda sem Tesseract instalado)
  - Critérios claros de revisão humana
"""

from pathlib import Path
from typing import Optional

# Tentativa de imports reais
try:
    import cv2
    import numpy as np
    import pytesseract
    from PIL import Image
    HAS_OCR = True
except ImportError:
    HAS_OCR = False


def preparar_imagem(caminho: str):
    """
    Pré-processamento (a lição da professora de OpenCV no livro):
    'Antes de melhorar a inteligência... melhore a visão.'
    """
    img = cv2.imread(caminho)
    if img is None:
        raise ValueError(f"Imagem inválida: {caminho}")
    cinza = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(cinza, (3, 3), 0)
    _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return img, thresh


def extrair_texto_ocr(caminho: str) -> str:
    _, thresh = preparar_imagem(caminho)
    return pytesseract.image_to_string(thresh, lang="por")


def localizar_zona_assinatura(img):
    """Região de interesse: faixa inferior direita do documento."""
    h, w = img.shape[:2]
    y1, y2 = int(h * 0.70), int(h * 0.95)
    x1, x2 = int(w * 0.35), int(w * 0.95)
    return img[y1:y2, x1:x2], (x1, y1, x2, y2)


def detectar_assinatura_na_linha(caminho: str) -> dict:
    img = cv2.imread(caminho)
    recorte, regiao = localizar_zona_assinatura(img)
    cinza = cv2.cvtColor(recorte, cv2.COLOR_BGR2GRAY)
    _, binaria = cv2.threshold(cinza, 180, 255, cv2.THRESH_BINARY_INV)
    contornos, _ = cv2.findContours(binaria, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contornos:
        return {"assinatura_detectada": False, "na_linha": False, "area": 0.0}
    maior = max(contornos, key=cv2.contourArea)
    area = float(cv2.contourArea(maior))
    ok = area > 300
    return {
        "assinatura_detectada": ok,
        "na_linha": ok,
        "area": area,
        "regiao_verificada": regiao,
    }


def processar_aceite(caminho: Optional[str] = None) -> dict:
    """
    Pipeline completo.
    Se não houver imagem/Tesseract, roda modo simulado (PLUS didático).
    """
    if caminho and HAS_OCR:
        try:
            texto = extrair_texto_ocr(caminho)
            assinatura = detectar_assinatura_na_linha(caminho)
            cnpj_ok = "cnpj" in texto.lower()
            nota_ok = "nota" in texto.lower() or "nf" in texto.lower()
            status = (
                "OK — seguir para sistema"
                if (cnpj_ok and nota_ok and assinatura["na_linha"])
                else "REVISÃO HUMANA"
            )
            return {
                "modo": "ocr_real",
                "texto_extraido": texto[:300],
                "cnpj_encontrado": cnpj_ok,
                "nota_encontrada": nota_ok,
                **assinatura,
                "status": status,
            }
        except Exception as e:
            return {"modo": "erro", "status": f"Falha OCR: {e}"}

    # Modo simulado — sempre funciona para estudo
    return {
        "modo": "simulado",
        "texto_extraido": "NF 12345\nCNPJ 12.345.678/0001-99\nCliente: Mercado Bom Preço",
        "cnpj_encontrado": True,
        "nota_encontrada": True,
        "assinatura_detectada": True,
        "na_linha": True,
        "area": 1250.0,
        "status": "OK — seguir para sistema",
    }


if __name__ == "__main__":
    print(f"OCR real disponível: {HAS_OCR}\n")
    resultado = processar_aceite()
    for k, v in resultado.items():
        print(f"  {k}: {v}")

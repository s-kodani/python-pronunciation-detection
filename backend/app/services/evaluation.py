"""
発音評価サービス
期待される音素と実際の音素を比較して発音精度を計算
"""
import logging

logger = logging.getLogger(__name__)


def compare_phonemes(expected: str, actual: str) -> float:
    """
    期待される音素と実際の音素を比較して発音精度を計算する

    Args:
        expected: 期待される音素文字列
        actual: 実際に発音された音素文字列

    Returns:
        発音精度（パーセンテージ）

    Raises:
        ValueError: 期待される音素が空の場合
    """
    if not expected:
        raise ValueError("Expected phonemes cannot be empty")

    try:
        # 位置ごとに音素を比較し、一致する数をカウント
        match_count = sum(1 for a, b in zip(expected, actual) if a == b)
        # 一致率をパーセンテージで計算
        accuracy = (match_count / len(expected)) * 100 if expected else 0.0
        logger.info(f"Pronunciation accuracy: {accuracy:.2f}% (matches: {match_count}/{len(expected)})")
        return round(accuracy, 2)
    except Exception as e:
        logger.error(f"Error during phoneme comparison: {str(e)}")
        raise Exception(f"Phoneme comparison failed: {str(e)}") from e

import re
from collections import Counter
from typing import Dict, List
from urllib.parse import urlparse

import requests


class TextPreprocessor:
    def __init__(self):
        self.stop_words = {
            "the", "and", "to", "of", "a", "in", "it", "is", "i", "you", "he",
            "she", "they", "we", "was", "were", "be", "been", "being", "for",
            "on", "with", "as", "at", "by", "an", "or", "that", "this", "from",
            "but", "not", "are", "his", "her", "their", "my", "our", "your",
            "me", "him", "them", "said", "had", "have", "has", "do", "did",
            "so", "no", "if", "out", "up", "all", "one", "would", "there",
            "what", "when", "who", "which", "into", "then", "than", "could",
            "should", "about", "over", "again", "very"
        }

    def fetch_from_url(self, url: str) -> str:
        """
        Fetch text content from a URL (especially Project Gutenberg)
        """
        if not url or not isinstance(url, str):
            raise ValueError("A valid URL is required.")

        parsed = urlparse(url)
        if parsed.scheme not in ("http", "https"):
            raise ValueError("URL must start with http:// or https://")

        if not parsed.path.lower().endswith(".txt"):
            raise ValueError("URL must point to a .txt file")

        try:
            response = requests.get(url, timeout=20)
            response.raise_for_status()
            return response.text
        except requests.RequestException as exc:
            raise Exception(f"Could not fetch text from URL: {exc}") from exc

    def remove_gutenberg_boilerplate(self, text: str) -> str:
        """
        Remove standard Project Gutenberg header and footer.
        """
        if not text:
            return ""

        start_patterns = [
            r"\*\*\* START OF THE PROJECT GUTENBERG EBOOK .*? \*\*\*",
            r"\*\*\* START OF THIS PROJECT GUTENBERG EBOOK .*? \*\*\*",
            r"\*\*\*START OF THE PROJECT GUTENBERG EBOOK .*?\*\*\*",
            r"\*\*\*START OF THIS PROJECT GUTENBERG EBOOK .*?\*\*\*",
        ]

        end_patterns = [
            r"\*\*\* END OF THE PROJECT GUTENBERG EBOOK .*? \*\*\*",
            r"\*\*\* END OF THIS PROJECT GUTENBERG EBOOK .*? \*\*\*",
            r"\*\*\*END OF THE PROJECT GUTENBERG EBOOK .*?\*\*\*",
            r"\*\*\*END OF THIS PROJECT GUTENBERG EBOOK .*?\*\*\*",
        ]

        for pattern in start_patterns:
            match = re.search(pattern, text, flags=re.IGNORECASE | re.DOTALL)
            if match:
                text = text[match.end():]
                break

        for pattern in end_patterns:
            match = re.search(pattern, text, flags=re.IGNORECASE | re.DOTALL)
            if match:
                text = text[:match.start()]
                break

        return text.strip()

    def remove_front_matter(self, text: str) -> str:
        """
        Remove title pages, edition info, contents, and similar front matter.
        Tries to begin at the first real chapter/body section.
        """
        if not text:
            return ""

        # Normalize line endings first
        text = text.replace("\r\n", "\n").replace("\r", "\n")

        # Remove bracketed illustration notes like [Illustration]
        text = re.sub(r"\[.*?\]", " ", text)

        # Remove obvious ebook metadata lines
        lines = [line.strip() for line in text.split("\n")]

        filtered_lines = []
        for line in lines:
            lower = line.lower()

            if not line:
                filtered_lines.append("")
                continue

            if any(bad in lower for bad in [
                "project gutenberg",
                "produced by",
                "transcribed by",
                "transcriber",
                "illustration",
                "millennium fulcrum edition",
                "distributed proofreaders",
                "http://",
                "https://",
                "copyright",
                "release date:",
                "language:",
                "character set encoding:",
                "encoding:",
                "title:",
                "author:",
                "ebook no.",
                "e-text prepared by",
            ]):
                continue

            filtered_lines.append(line)

        text = "\n".join(filtered_lines)

        # Remove contents block if present
        contents_patterns = [
            r"contents\s+chapter .*?(?=(chapter i\.|chapter 1|down the rabbit-hole|alice was beginning|once upon))",
            r"contents.*?(?=(chapter i\.|chapter 1|down the rabbit-hole|alice was beginning|once upon))",
        ]

        for pattern in contents_patterns:
            text = re.sub(pattern, "", text, flags=re.IGNORECASE | re.DOTALL)

        # Try to start at first real chapter heading or first narrative sentence
        start_markers = [
            r"CHAPTER I\.?\s+Down the Rabbit[- ]Hole",
            r"Chapter I\.?\s+Down the Rabbit[- ]Hole",
            r"CHAPTER I\b",
            r"Chapter I\b",
            r"\bAlice was beginning to get very tired\b",
            r"\bOnce upon a time\b",
        ]

        start_index = None
        for pattern in start_markers:
            match = re.search(pattern, text, flags=re.IGNORECASE)
            if match:
                start_index = match.start()
                break

        if start_index is not None:
            text = text[start_index:]

        return text.strip()

    def clean_text(self, text: str) -> str:
        """
        Clean text for analysis and display.
        """
        if not text:
            return ""

        text = self.remove_gutenberg_boilerplate(text)
        text = self.remove_front_matter(text)

        # Normalize whitespace
        text = text.replace("\r\n", "\n").replace("\r", "\n")

        # Keep paragraph boundaries temporarily
        text = re.sub(r"\n\s*\n+", "\n\n", text)

        # Remove single newlines inside paragraphs
        text = re.sub(r"(?<!\n)\n(?!\n)", " ", text)

        # Collapse spaces
        text = re.sub(r"[ \t]+", " ", text)

        # Collapse repeated blank lines
        text = re.sub(r"\n{3,}", "\n\n", text)

        return text.strip()

    def get_sentences(self, text: str) -> List[str]:
        """
        Split text into sentences using a simple regex.
        """
        if not text:
            return []

        text = text.replace("\n", " ")
        sentences = re.split(r'(?<=[.!?])\s+', text.strip())
        return [sentence.strip() for sentence in sentences if sentence.strip()]

    def get_words(self, text: str) -> List[str]:
        """
        Extract words from text.
        """
        if not text:
            return []

        return re.findall(r"\b[a-zA-Z']+\b", text.lower())

    def get_text_statistics(self, text: str) -> Dict:
        """
        Calculate basic statistics about the text.
        """
        cleaned_text = self.clean_text(text)
        words = self.get_words(cleaned_text)
        sentences = self.get_sentences(cleaned_text)

        total_characters = len(cleaned_text)
        total_words = len(words)
        total_sentences = len(sentences)

        avg_word_length = round(
            sum(len(word) for word in words) / total_words, 2
        ) if total_words > 0 else 0

        avg_sentence_length = round(
            total_words / total_sentences, 2
        ) if total_sentences > 0 else 0

        filtered_words = [word for word in words if word not in self.stop_words]
        common_words = Counter(filtered_words).most_common(10)

        return {
            "total_characters": total_characters,
            "total_words": total_words,
            "total_sentences": total_sentences,
            "avg_word_length": avg_word_length,
            "avg_sentence_length": avg_sentence_length,
            "most_common_words": [
                {"word": word, "count": count}
                for word, count in common_words
            ],
        }

    def create_summary(self, text: str, num_sentences: int = 3) -> str:
        """
        Create a simple extractive summary using the first meaningful
        story sentences after cleaning.
        """
        if not text or num_sentences <= 0:
            return ""

        cleaned_text = self.clean_text(text)
        sentences = self.get_sentences(cleaned_text)

        useful_sentences = []
        for sentence in sentences:
            s = sentence.strip()
            lower = s.lower()

            if len(s.split()) < 8:
                continue

            if any(bad in lower for bad in [
                "chapter i",
                "chapter ii",
                "chapter iii",
                "contents",
                "illustration",
                "project gutenberg",
                "ebook",
                "edition",
            ]):
                continue

            # Skip lines that are mostly uppercase headings
            letters = [c for c in s if c.isalpha()]
            if letters:
                uppercase_ratio = sum(1 for c in letters if c.isupper()) / len(letters)
                if uppercase_ratio > 0.6:
                    continue

            useful_sentences.append(s)

            if len(useful_sentences) == num_sentences:
                break

        if useful_sentences:
            return " ".join(useful_sentences)

        return "Summary unavailable."
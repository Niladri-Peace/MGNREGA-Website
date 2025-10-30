import { useState, useEffect, useCallback } from 'react';

export interface UseSpeechReturn {
  speak: (text: string, lang?: string) => void;
  cancel: () => void;
  pause: () => void;
  resume: () => void;
  speaking: boolean;
  supported: boolean;
  voices: SpeechSynthesisVoice[];
}

/**
 * Hook for Text-to-Speech functionality
 * Essential for low-literacy users
 */
export const useSpeech = (): UseSpeechReturn => {
  const [speaking, setSpeaking] = useState<boolean>(false);
  const [supported, setSupported] = useState<boolean>(false);
  const [voices, setVoices] = useState<SpeechSynthesisVoice[]>([]);

  useEffect(() => {
    if (typeof window !== 'undefined' && 'speechSynthesis' in window) {
      setSupported(true);
      
      // Load voices
      const loadVoices = () => {
        const availableVoices = window.speechSynthesis.getVoices();
        setVoices(availableVoices);
      };

      loadVoices();
      
      // Voices might load asynchronously
      if (window.speechSynthesis.onvoiceschanged !== undefined) {
        window.speechSynthesis.onvoiceschanged = loadVoices;
      }
    }
  }, []);

  const speak = useCallback(
    (text: string, lang: string = 'hi-IN') => {
      if (!supported) {
        console.warn('Speech synthesis not supported');
        return;
      }

      // Cancel any ongoing speech
      window.speechSynthesis.cancel();

      const utterance = new SpeechSynthesisUtterance(text);
      utterance.lang = lang;
      utterance.rate = 0.9; // Slightly slower for better comprehension
      utterance.pitch = 1;
      utterance.volume = 1;

      // Try to find a voice for the specified language
      const voice = voices.find((v) => v.lang === lang || v.lang.startsWith(lang.split('-')[0]));
      if (voice) {
        utterance.voice = voice;
      }

      utterance.onstart = () => setSpeaking(true);
      utterance.onend = () => setSpeaking(false);
      utterance.onerror = (event) => {
        console.error('Speech synthesis error:', event);
        setSpeaking(false);
      };

      window.speechSynthesis.speak(utterance);
    },
    [supported, voices]
  );

  const cancel = useCallback(() => {
    if (supported) {
      window.speechSynthesis.cancel();
      setSpeaking(false);
    }
  }, [supported]);

  const pause = useCallback(() => {
    if (supported && speaking) {
      window.speechSynthesis.pause();
    }
  }, [supported, speaking]);

  const resume = useCallback(() => {
    if (supported && speaking) {
      window.speechSynthesis.resume();
    }
  }, [supported, speaking]);

  return {
    speak,
    cancel,
    pause,
    resume,
    speaking,
    supported,
    voices,
  };
};

/**
 * Language codes for Indian languages
 */
export const INDIAN_LANGUAGES = {
  hindi: 'hi-IN',
  english: 'en-IN',
  tamil: 'ta-IN',
  telugu: 'te-IN',
  bengali: 'bn-IN',
  marathi: 'mr-IN',
  gujarati: 'gu-IN',
  kannada: 'kn-IN',
  malayalam: 'ml-IN',
  punjabi: 'pa-IN',
  odia: 'or-IN',
  assamese: 'as-IN',
};

/**
 * Helper function to get simple explanations for metrics
 */
export const getMetricExplanation = (metric: string, value: number, lang: string = 'en'): string => {
  const explanations: Record<string, Record<string, string>> = {
    households: {
      en: `${value} families got work under MGNREGA`,
      hi: `मनरेगा के तहत ${value} परिवारों को काम मिला`,
    },
    person_days: {
      en: `${value} days of work were provided`,
      hi: `${value} दिनों का काम दिया गया`,
    },
    works_completed: {
      en: `${value} projects were completed`,
      hi: `${value} परियोजनाएं पूरी हुईं`,
    },
    funds_utilized: {
      en: `${value} rupees were spent on wages and materials`,
      hi: `मजदूरी और सामग्री पर ${value} रुपये खर्च किए गए`,
    },
  };

  return explanations[metric]?.[lang] || `${metric}: ${value}`;
};

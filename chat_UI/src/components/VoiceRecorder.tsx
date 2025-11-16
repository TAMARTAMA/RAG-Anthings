import React, { useState, useRef } from "react";
import { Mic, Square } from "lucide-react";
const TRANSCRIBE_URL = import.meta.env.VITE_TRANSCRIBE_URL;


interface VoiceRecorderProps {
  inputRef: React.RefObject<HTMLTextAreaElement>;
  onTranscription: (text: string) => void;
}

const VoiceRecorder: React.FC<VoiceRecorderProps> = ({
  inputRef,
  onTranscription,
}) => {
  const [isRecording, setIsRecording] = useState(false);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const chunksRef = useRef<Blob[]>([]);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const recorder = new MediaRecorder(stream);
      mediaRecorderRef.current = recorder;
      chunksRef.current = [];

      recorder.ondataavailable = (e) => {
        if (e.data.size > 0) chunksRef.current.push(e.data);
      };

      recorder.onstop = async () => {
        const blob = new Blob(chunksRef.current, { type: "audio/webm" });
        await uploadAndTranscribe(blob);

        if (inputRef.current) {
          inputRef.current.focus();
        }
      };

      recorder.start();
      setIsRecording(true);
    } catch (err) {
      console.error("Microphone access error:", err);
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    }
  };

  const uploadAndTranscribe = async (blob: Blob) => {
    try {
      const formData = new FormData();
      formData.append("file", blob, "recording.webm");

      const response = await fetch(`${TRANSCRIBE_URL}`, {
        method: "POST",
        body: formData 
      });


      const data = await response.json();
      if (data.text) onTranscription(data.text);
    } catch (err) {
      console.error("Error sending recording:", err);
    }
  };

  return (
    <button
      type="button"

      onClick={isRecording ? stopRecording : startRecording}
      onKeyDown={(e) => e.preventDefault()} 
      className={`p-3 rounded-xl transition-colors duration-200 ${
        isRecording ? "bg-red-600" : "bg-gray-200 hover:bg-gray-300"
      }`}
    >
      {isRecording ? (
        <Square className="w-5 h-5 text-white" />
      ) : (
        <Mic className="w-5 h-5 text-gray-700" />
      )}
    </button>
  );
};

export default VoiceRecorder;

'use client';

import { useState, FormEvent, KeyboardEvent } from 'react';

interface InputBarProps {
  onSend: (message: string) => void;
  loading: boolean;
}

export default function InputBar({ onSend, loading }: InputBarProps) {
  const [value, setValue] = useState('');
  const [validationError, setValidationError] = useState('');

  const handleSubmit = (e?: FormEvent) => {
    if (e) e.preventDefault();

    if (!value.trim()) {
      setValidationError('Message cannot be empty.');
      return;
    }

    setValidationError('');
    onSend(value.trim());
    setValue('');
  };

  return (
    <form
      onSubmit={handleSubmit}
      style={{ display: 'flex', flexDirection: 'column', gap: '4px', padding: '12px', borderTop: '1px solid #e0e0e0' }}
    >
      <div style={{ display: 'flex', gap: '8px' }}>
        <input
          type="text"
          value={value}
          onChange={(e) => {
            setValue(e.target.value);
            if (validationError) setValidationError('');
          }}
          disabled={loading}
          placeholder="Type a message..."
          style={{
            flex: 1,
            padding: '8px 12px',
            fontSize: '14px',
            border: validationError ? '1px solid #e53e3e' : '1px solid #ccc',
            borderRadius: '6px',
            outline: 'none',
          }}
        />
        <button
          type="submit"
          disabled={loading}
          style={{
            padding: '8px 16px',
            fontSize: '14px',
            backgroundColor: loading ? '#a0aec0' : '#3182ce',
            color: '#fff',
            border: 'none',
            borderRadius: '6px',
            cursor: loading ? 'not-allowed' : 'pointer',
            minWidth: '72px',
          }}
        >
          {loading ? '⟳' : 'Send'}
        </button>
      </div>
      {validationError && (
        <span style={{ fontSize: '12px', color: '#e53e3e' }}>{validationError}</span>
      )}
    </form>
  );
}

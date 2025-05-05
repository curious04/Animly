import React, { useState } from 'react';
import {
    Container,
    TextField,
    Button,
    Paper,
    Typography,
    Box,
    CircularProgress,
    Snackbar,
    Alert,
} from '@mui/material';
import axios from 'axios';

function App() {
    const [prompt, setPrompt] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [generatedCode, setGeneratedCode] = useState('');
    const [videoUrl, setVideoUrl] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');
        setGeneratedCode('');
        setVideoUrl('');

        try {
            const response = await axios.post('http://localhost:5000/generate', {
                prompt: prompt
            });

            if (response.data.success) {
                setGeneratedCode(response.data.code);
                // Construct the full video URL
                const fullVideoUrl = `http://localhost:5000${response.data.video_path}`;
                setVideoUrl(fullVideoUrl);
            } else {
                setError(response.data.error || 'Failed to generate animation');
            }
        } catch (err) {
            console.error('Error:', err);
            setError(err.response?.data?.error || err.message || 'An error occurred');
        } finally {
            setLoading(false);
        }
    };

    return (
        <Container maxWidth="md" sx={{ py: 4 }}>
            <Typography variant="h3" component="h1" gutterBottom align="center">
                AnimX - AI Animation Generator
            </Typography>

            <Paper elevation={3} sx={{ p: 3, mb: 3 }}>
                <form onSubmit={handleSubmit}>
                    <TextField
                        fullWidth
                        multiline
                        rows={4}
                        variant="outlined"
                        label="Describe your animation"
                        value={prompt}
                        onChange={(e) => setPrompt(e.target.value)}
                        placeholder="Example: Create a bouncing ball animation with a shadow"
                        sx={{ mb: 2 }}
                    />
                    <Button
                        type="submit"
                        variant="contained"
                        color="primary"
                        fullWidth
                        disabled={loading || !prompt}
                        sx={{ height: 48 }}
                    >
                        {loading ? <CircularProgress size={24} /> : 'Generate Animation'}
                    </Button>
                </form>
            </Paper>

            {generatedCode && (
                <Paper elevation={3} sx={{ p: 3, mb: 3 }}>
                    <Typography variant="h6" gutterBottom>
                        Generated Code:
                    </Typography>
                    <Box
                        component="pre"
                        sx={{
                            p: 2,
                            bgcolor: 'grey.100',
                            borderRadius: 1,
                            overflow: 'auto',
                            maxHeight: '300px',
                        }}
                    >
                        {generatedCode}
                    </Box>
                </Paper>
            )}

            {videoUrl && (
                <Paper elevation={3} sx={{ p: 3 }}>
                    <Typography variant="h6" gutterBottom>
                        Generated Animation:
                    </Typography>
                    <video
                        controls
                        width="100%"
                        style={{ borderRadius: '4px' }}
                        key={videoUrl} // Force re-render when URL changes
                    >
                        <source src={videoUrl} type="video/mp4" />
                        Your browser does not support the video tag.
                    </video>
                </Paper>
            )}

            <Snackbar
                open={!!error}
                autoHideDuration={6000}
                onClose={() => setError('')}
            >
                <Alert severity="error" onClose={() => setError('')}>
                    {error}
                </Alert>
            </Snackbar>
        </Container>
    );
}

export default App; 
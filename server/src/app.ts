import express from 'express';
import cors from 'cors';
import pdfRoutes from './routes/pdfRoutes';
import flashcardRoutes from './routes/flashcardRoutes';
import chatRoutes from './routes/chatRoutes';

const app = express();
app.use(cors());
app.use(express.json());
app.use('/pdf', pdfRoutes);
app.use('/flashcards', flashcardRoutes);
app.use('/chat', chatRoutes);

export default app;
import express from 'express';
import { PrismaClient } from '@prisma/client';

const router = express.Router()
const prisma = new PrismaClient();

// routes...

export default router;
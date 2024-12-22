import { createAsyncThunk } from "@reduxjs/toolkit";
import { loadTodos } from "../services/sliceService";

export const loadTodosAction = createAsyncThunk(
  "todo/load",
  async (_, thunkAPI) => {
    try {
      const response = await loadTodos();
      if (response.data && response.status === 200) {
        return thunkAPI.fulfillWithValue(response.data);
      }
      return thunkAPI.rejectWithValue({
        message: "failed to get admin blogs",
      });
    } catch (error) {
      console.log("[!] Error at loading todos ", error);
      return thunkAPI.rejectWithValue({
        message: "Failed to get admin blogs",
      });
    }
  }
);

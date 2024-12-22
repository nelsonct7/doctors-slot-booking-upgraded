import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import { TodoType } from "../../types/todo";
import { loadTodosAction } from "../middlewares/todoMiddleware";

// Define a type for the slice state
interface CounterState {
  loading: boolean;
  todoList: TodoType[];
}

// Define the initial state using that type
const initialState: CounterState = {
  loading: true,
  todoList: [],
};

export const todoSlice = createSlice({
  name: "todo",
  // `createSlice` will infer the state type from the `initialState` argument
  initialState,
  reducers: {
    setLoading: (state, { payload }) => {
      state.loading = payload;
    },
  },
  extraReducers: (builder) => {
    // loading public courses
    builder.addCase(loadTodosAction.pending, (state) => {
      state.loading = true;
    });
    builder.addCase(
        loadTodosAction.fulfilled,
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      (state, action: PayloadAction<any>) => {
        state.loading=false;
        state.todoList=action.payload
      }
    );
    builder.addCase(
        loadTodosAction.rejected,
      (state) => {
        state.loading = false;
        state.todoList = [];
      }
    );
  },
});

export const { setLoading } = todoSlice.actions;

export default todoSlice.reducer;

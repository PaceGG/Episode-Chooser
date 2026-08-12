import { database, onValue, ref } from "@/api/firebase";
import { ThemedText } from "@/components/themed-text";
import { ThemedView } from "@/components/themed-view";
import { useEffect, useState } from "react";
import { Platform, StyleSheet } from "react-native";

export default function Launcher() {
  const [counter, setCounter] = useState(0);
  const [status, setStatus] = useState("inactive");
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const statusRef = ref(database, "status");

    const unsubscribe = onValue(statusRef, (snapshot) => {
      const data = snapshot.val();

      if (data) {
        setStatus(data.status || "inactive");
        setCounter(data.counter || 0);
      } else {
        setStatus("inactive");
        setCounter(0);
      }

      setIsLoading(false);
    });

    return () => unsubscribe();
  }, []);

  return (
    <ThemedView style={styles.body}>
      <ThemedText style={styles.h1}>Launcher</ThemedText>
      <ThemedText>Status: "{status}"</ThemedText>
    </ThemedView>
  );
}

const styles = StyleSheet.create({
  body: {
    flex: 1,
    paddingTop: 48,
    paddingHorizontal: 16,
    backgroundColor: "#222",
  },
  h1: {
    fontSize: 35,
    textAlign: "center",
  },
});

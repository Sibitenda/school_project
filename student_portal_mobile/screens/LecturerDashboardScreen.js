import React, { useEffect, useState } from "react";
import { View, Text, Button, StyleSheet, ScrollView } from "react-native";
import { fetchDashboard } from "../api/client";

export default function LecturerDashboardScreen({ route, navigation }) {
  const { token } = route.params;
  const [data, setData] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      const res = await fetchDashboard(token);
      setData(res);
    };
    fetchData();
  }, []);

  if (!data) return <Text>Loading lecturer dashboard...</Text>;

  return (
    <ScrollView style={styles.container}>
      <Text style={styles.title}>📚 Lecturer Dashboard</Text>
      <Text>Name: {data.profile?.name}</Text>

      <Text style={styles.section}>Courses You Teach:</Text>
      {(data.courses || []).map((c, i) => (
        <Text key={i}>- {c.code}: {c.name}</Text>
      ))}

      <Text style={styles.section}>Marks You've Entered:</Text>
      {(data.marks || []).map((m, i) => (
        <Text key={i}>{m.student__name} - {m.course__name} ({m.score}%)</Text>
      ))}

      <Button title="Logout" onPress={() => navigation.goBack()} />
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 20, backgroundColor: "#fff" },
  title: { fontSize: 24, fontWeight: "bold", marginBottom: 10 },
  section: { fontWeight: "bold", marginTop: 15 },
});

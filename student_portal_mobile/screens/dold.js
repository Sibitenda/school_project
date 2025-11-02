import React, { useEffect, useState } from "react";
import { View, Text, Button, StyleSheet, ScrollView } from "react-native";
import { fetchDashboard } from "../api/client";

export default function DashboardScreen({ route, navigation }) {
  const { token } = route.params;
  const [data, setData] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await fetchDashboard(token);
        setData(res);
      } catch (err) {
        console.error(err);
      }
    };
    fetchData();
  }, []);

 return (
  <ScrollView style={styles.container}>
    <Text style={styles.title}>📘 Dashboard</Text>
    <Text>Name: {data.profile?.name}</Text>
    <Text>Role: {data.profile?.role}</Text>

    {/* Role-based rendering */}
    {data.profile?.role === "Admin" && (
      <>
        <Text style={styles.section}>👑 Admin Summary</Text>
        {Object.entries(data.summary || {}).map(([key, val]) => (
          <Text key={key}>{key}: {val}</Text>
        ))}
      </>
    )}

    {data.profile?.role === "Lecturer" && (
      <>
        <Text style={styles.section}>📚 Your Courses</Text>
        {(data.courses || []).map((c, i) => (
          <Text key={i}>{c.code} - {c.name}</Text>
        ))}
        <Text style={styles.section}>🧑‍🎓 Marks Given</Text>
        {(data.marks || []).map((m, i) => (
          <Text key={i}>{m.student__name}: {m.course__name} ({m.score}%)</Text>
        ))}
      </>
    )}

    {data.profile?.role === "Student" && (
      <>
        <Text style={styles.section}>🎓 Your Marks</Text>
        {(data.marks || []).map((m, i) => (
          <Text key={i}>{m.course__name}: {m.score}% ({m.grade})</Text>
        ))}
        <Text style={styles.section}>🏆 Achievements</Text>
        {(data.achievements || []).map((a, i) => (
          <Text key={i}>{a.title} - {a.description}</Text>
        ))}
      </>
    )}

    <Button title="Logout" onPress={() => navigation.goBack()} />
  </ScrollView>
);

}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 20, backgroundColor: "#fff" },
  title: { fontSize: 24, fontWeight: "bold", marginBottom: 10 },
});

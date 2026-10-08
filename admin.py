import streamlit as st
import pandas as pd
from utils import auth


def render():
    user = st.session_state.get("user")
    if not user or user["role"] != "admin":
        st.error("Admins only.")
        return

    st.markdown('<h1 class="gradient-header">🛠️ Admin Panel</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Create users, monitor their progress, and manage accounts.</p>', unsafe_allow_html=True)

    if auth.verify("admin", "admin123"):
        st.warning("The default admin password (admin123) is still in use. Change it in the sidebar → Account.")

    users = auth.list_users()
    rows = []
    for u in users:
        sc = auth.load_progress(u["username"]).get("scores", {})
        att = sum(v.get("attempted", 0) for v in sc.values())
        cor = sum(v.get("correct", 0) for v in sc.values())
        rows.append({"Username": u["username"], "Name": u["full_name"], "Role": u["role"], "Created": u["created"],
                     "Attempted": att, "Correct": cor, "Accuracy %": round(cor / att * 100, 1) if att else 0})
    df = pd.DataFrame(rows)

    t1, t2, t3, t4 = st.tabs(["👥 Monitor Users", "➕ Create User", "⚙️ Manage User", "💾 Backup"])

    with t1:
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Users", len(df))
        c2.metric("Total Attempts", int(df["Attempted"].sum()) if len(df) else 0)
        c3.metric("Avg Accuracy", f"{df['Accuracy %'].mean():.1f}%" if len(df) else "0%")
        st.dataframe(df, width="stretch", hide_index=True)
        pick = st.selectbox("View module-wise progress of", [u["username"] for u in users], key="adm_view")
        sc = auth.load_progress(pick).get("scores", {})
        if sc:
            mdf = pd.DataFrame([{"Module": m, "Attempted": v["attempted"], "Correct": v["correct"],
                                 "Accuracy %": round(v["correct"] / v["attempted"] * 100, 1) if v["attempted"] else 0}
                                for m, v in sc.items()])
            st.dataframe(mdf, width="stretch", hide_index=True)
        else:
            st.info("This user has no activity yet.")

    with t2:
        with st.form("create_user", clear_on_submit=True):
            nu = st.text_input("Username")
            nn = st.text_input("Full name (optional)")
            npw = st.text_input("Password", type="password")
            nr = st.selectbox("Role", ["user", "admin"])
            if st.form_submit_button("Create user"):
                ok, msg = auth.create_user(nu, npw, nr, nn)
                (st.success if ok else st.error)(msg)

    with t3:
        target = st.selectbox("Select user", [u["username"] for u in users], key="adm_target")
        npw = st.text_input("New password", type="password", key="adm_newpw")
        if st.button("Reset password"):
            ok, msg = auth.set_password(target, npw)
            (st.success if ok else st.error)(msg)
        role = st.selectbox("Role", ["user", "admin"], key="adm_role")
        if st.button("Change role"):
            ok, msg = auth.set_role(target, role)
            (st.success if ok else st.error)(msg)
        st.divider()
        confirm = st.checkbox(f"Yes, permanently delete '{target}' and their data")
        if st.button("Delete user", disabled=not confirm or target == user["username"]):
            ok, msg = auth.delete_user(target)
            (st.success if ok else st.error)(msg)
            if ok:
                st.rerun()
        if target == user["username"]:
            st.caption("You can't delete your own account while logged in.")

    with t4:
        st.info("On Streamlit Cloud the app's disk is wiped when the app is rebooted or redeployed. "
                "Download a backup after adding users, and restore it here if that happens.")
        st.download_button("⬇️ Download backup (JSON)", auth.export_all(), "backup.json", "application/json")
        up = st.file_uploader("Restore from backup", type="json")
        if up and st.button("Restore now"):
            try:
                n = auth.import_all(up.read().decode("utf-8"))
                st.success(f"Restored {n} users.")
            except Exception as e:
                st.error(f"Invalid backup file: {e}")
